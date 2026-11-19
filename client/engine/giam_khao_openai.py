"""Thiên Đạo Giám Khảo on any address that speaks the OpenAI chat-completions format: other
hosted providers, and a model running on the player's own machine (Ollama, LM Studio), which
needs no key and costs nothing.

These servers differ in what they accept, so this asks for the least: one chat completion,
with the verdict's JSON schema written into the instructions and `response_format` set to a
JSON object. A server that rejects `response_format` is asked once more without it. The
verdict is then checked like any other (giam_khao.parse_verdict): nothing here trusts that
the JSON is right.
"""
from __future__ import annotations

import json

import httpx

from .giam_khao import Completion, GraderConfig, GraderError, Prompt

TIMEOUT_S = 180.0
PING_TIMEOUT_S = 30.0
JSON_RULE_VI = ("Trả lời bằng đúng một đối tượng JSON theo lược đồ dưới đây, không thêm chữ nào "
                "trước hay sau, không bọc trong dấu ```:\n")


def _url(config: GraderConfig) -> str:
    return config.base_url.strip().rstrip("/") + "/chat/completions"


def _headers(config: GraderConfig) -> dict:
    headers = {"Content-Type": "application/json"}
    if config.key():
        headers["Authorization"] = f"Bearer {config.key()}"
    return headers


def _detail(response: httpx.Response) -> str:
    """The server's own words, short. Never the request (it holds the key)."""
    try:
        data = response.json()
        error = data.get("error") if isinstance(data, dict) else None
        if isinstance(error, dict):
            return str(error.get("message") or "")[:300]
        if isinstance(error, str):
            return error[:300]
    except ValueError:
        pass
    return response.text[:300]


def _raise_for(response: httpx.Response, model: str) -> None:
    status = response.status_code
    if status < 400:
        return
    if status == 401:
        raise GraderError("bad_key")
    if status == 403:
        raise GraderError("no_permission", _detail(response))
    if status == 404:
        raise GraderError("bad_model", f"{model}: {_detail(response)}")
    if status == 429:
        raise GraderError("rate_limit")
    raise GraderError("server" if status >= 500 else "bad_request", _detail(response))


class OpenAICompatibleProvider:
    def __init__(self, transport: httpx.BaseTransport | None = None):
        self._transport = transport     # a scripted server, for tests

    def _post(self, config: GraderConfig, body: dict, timeout: float) -> dict:
        try:
            with httpx.Client(transport=self._transport, timeout=timeout) as client:
                response = client.post(_url(config), headers=_headers(config), json=body)
                if response.status_code == 400 and "response_format" in body:
                    # some servers do not know response_format: the instructions still ask for JSON
                    body = {k: v for k, v in body.items() if k != "response_format"}
                    response = client.post(_url(config), headers=_headers(config), json=body)
        except httpx.TimeoutException:
            raise GraderError("timeout")
        except httpx.HTTPError:
            raise GraderError("network")
        _raise_for(response, body["model"])
        try:
            data = response.json()
        except ValueError:
            raise GraderError("unreadable", "the server did not answer with JSON")
        if not isinstance(data, dict):
            raise GraderError("unreadable", "the server did not answer with a JSON object")
        return data

    @staticmethod
    def _completion(data: dict, model: str) -> Completion:
        try:
            choice = data["choices"][0]
            text = choice["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise GraderError("unreadable", "no choices in the answer")
        if choice.get("finish_reason") == "length":
            raise GraderError("cut_off")
        if not isinstance(text, str) or not text.strip():
            raise GraderError("unreadable", "an empty answer")
        usage = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        return Completion(text=text, model=str(data.get("model") or model),
                          input_tokens=int(usage.get("prompt_tokens") or 0),
                          output_tokens=int(usage.get("completion_tokens") or 0))

    def complete(self, prompt: Prompt, schema: dict, config: GraderConfig) -> Completion:
        model = config.model_name()
        system = (f"{prompt.rules}\n\n{JSON_RULE_VI}{json.dumps(schema, ensure_ascii=False)}"
                  f"\n\n{prompt.essay}")
        body = {
            "model": model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt.answer}],
            "response_format": {"type": "json_object"},
        }
        return self._completion(self._post(config, body, TIMEOUT_S), model)

    def ping(self, config: GraderConfig) -> str:
        model = config.model_name()
        body = {"model": model,
                "messages": [{"role": "user", "content": "Trả lời đúng một chữ: ok"}]}
        return self._completion(self._post(config, body, PING_TIMEOUT_S), model).model
