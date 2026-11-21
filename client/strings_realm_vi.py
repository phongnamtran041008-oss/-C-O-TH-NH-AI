"""Chữ của Cổng Bí Cảnh về dải tu vi của một lượt (server/app/systems/realm_quai.py,
docs/BI_CANH_QUAI.md). Riêng một tệp để khỏi chạm vào strings_vi.py."""

REALM_BAND_PARTY = "Bí cảnh theo tu vi tổ đội: {band}"
REALM_BAND_SOLO = "Bí cảnh theo tu vi của con: {band}"


def band_line(row: dict) -> str:
    """The line the gate shows under a bí cảnh ('' when the server sent no band)."""
    band = row.get("band_vi")
    if not band:
        return ""
    return (REALM_BAND_PARTY if row.get("band_party") else REALM_BAND_SOLO).format(band=band)
