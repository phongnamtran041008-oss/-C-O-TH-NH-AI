"""Thiên Đạo Giám Khảo on Claude, through the official Anthropic SDK.

The SDK is an optional dependency: the game does not ship it and nothing imports it until a
player picks this provider (`pip install anthropic`). The request is one Messages call:

  * the rules and the essay go in `system`, with a cache breakpoint after the essay, so
    marking the same essay again reads them from the cache;
  * the learner's answer is the user message;
  * `output_config.format` holds the verdict's JSON schema, so the answer is always a
    verdict of the right shape;
  * `effort` is high: judging a proof is the kind of work where depth matters. Thinking is
    left to the model (adaptive is the default on the current models);
  * on the models that support it, the request opts in to server-side refusal fallbacks, so
    a declined request is re-run on a fallback model inside the same call.
"""
from __future__ import annotations

from .giam_khao import Completion, GraderConfig, GraderError, Prompt

MAX_TOKENS = 16000          # room for the thinking and the verdict, and still under the HTTP timeout
EFFORT = "high"
TIMEOUT_S = 180.0
MAX_RETRIES = 2
FALLBACK_BETA = "server-side-fallback-2026-07-01"
# Models whose refusals can be re-run server-side. Claude Haiku 5.5 has no server-side fallback.
FALLBACK_MODELS = frozenset({"claude-fable-5-2", "claude-fable-5-1", "claude-opus-5-5",
                             "claude-opus-5", "claude-sonnet-5-5"})
PING_MAX_TOKENS = 256


def _sdk():
    try:
        import anthropic
    except ImportError:
        raise GraderError("no_sdk", "pip install anthropic")
    return anthropic


def _detail(exc) -> str:
    """The API's own sentence about what went wrong, short. Never the request."""
    body = getattr(exc, "body", None)
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict) and error.get("message"):
        return str(error["message"])[:300]
    return str(getattr(exc, "message", "") or "")[:300]


def _total_input(usage) -> int:
    """What was read, cached or not."""
    return sum(int(getattr(usage, name, 0) or 0) for name in
               ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))


class ClaudeProvider:
    def __init__(self, client=None):
        self._client = client       # a ready client, for tests; else one is made per call

    def _make_client(self, anthropic, config: GraderConfig):
        if self._client is not None:
            return self._client
        return anthropic.Anthropic(api_key=config.key(), timeout=TIMEOUT_S, max_retries=MAX_RETRIES)

    def _call(self, config: GraderConfig, **kwargs):
        anthropic = _sdk()
        client = self._make_client(anthropic, config)
        model = config.model_name()
        try:
            if model in FALLBACK_MODELS:
                return client.beta.messages.create(model=model, betas=[FALLBACK_BETA],
                                                   fallbacks="default", **kwargs)
            return client.messages.create(model=model, **kwargs)
        except anthropic.APITimeoutError:
            raise GraderError("timeout")
        except anthropic.AuthenticationError:
            raise GraderError("bad_key")
        except anthropic.PermissionDeniedError as exc:
            raise GraderError("no_permission", _detail(exc))
        except anthropic.NotFoundError:
            raise GraderError("bad_model", model)
        except anthropic.RateLimitError:
            raise GraderError("rate_limit")
        except anthropic.BadRequestError as exc:
            raise GraderError("bad_request", _detail(exc))
        except anthropic.APIStatusError as exc:
            raise GraderError("server" if exc.status_code >= 500 else "bad_request", _detail(exc))
        except anthropic.APIConnectionError:
            raise GraderError("network")

    @staticmethod
    def _text(response) -> str:
        if response.stop_reason == "refusal":
            details = getattr(response, "stop_details", None)
            raise GraderError("refused", str(getattr(details, "category", "") or ""))
        if response.stop_reason == "max_tokens":
            raise GraderError("cut_off")
        for block in response.content:
            if block.type == "text":
                return block.text
        raise GraderError("unreadable", "no text in the answer")

    def complete(self, prompt: Prompt, schema: dict, config: GraderConfig) -> Completion:
        response = self._call(
            config,
            max_tokens=MAX_TOKENS,
            system=[
                {"type": "text", "text": prompt.rules},
                {"type": "text", "text": prompt.essay, "cache_control": {"type": "ephemeral"}},
            ],
            messages=[{"role": "user", "content": prompt.answer}],
            output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
        )
        return Completion(text=self._text(response), model=response.model,
                          input_tokens=_total_input(response.usage),
                          output_tokens=int(response.usage.output_tokens or 0))

    def ping(self, config: GraderConfig) -> str:
        response = self._call(
            config,
            max_tokens=PING_MAX_TOKENS,
            messages=[{"role": "user", "content": "Trả lời đúng một chữ: ok"}],
            output_config={"effort": "low"},
        )
        # An answer of any kind proves the key and the model name; a short answer cut off by
        # max_tokens (the model thinks first) is still an answer.
        return response.model
