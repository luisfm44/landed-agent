from packages.tools.pricing.calculate_import_cost_tool import calculate_import_cost
from packages.tools.pricing.get_local_price_tool import get_local_price


def test_get_local_price_returns_normalized_dict(monkeypatch):
    def fake_call_landed_api(path, params=None, trace_id=None):
        return {
            "ok": True,
            "trace_id": trace_id,
            "source": "landed_api",
            "data": {
                "local_price_usd": 245,
                "local_price_cop": 980000,
            },
        }

    monkeypatch.setattr(
        "packages.tools.pricing.get_local_price_tool.call_landed_api",
        fake_call_landed_api,
    )

    result = get_local_price("dt 770 pro")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "landed_backend:/compare"
    assert result["data"] is not None
    assert result["data"]["tool"] == "get_local_price"


def test_calculate_import_cost_returns_normalized_dict(monkeypatch):
    def fake_call_landed_api(path, params=None, trace_id=None):
        return {
            "ok": True,
            "trace_id": trace_id,
            "source": "landed_api",
            "data": {
                "total_landed_cost_usd": 236,
                "shipping_usd": 35,
                "taxes_usd": 32,
            },
        }

    monkeypatch.setattr(
        "packages.tools.pricing.calculate_import_cost_tool.call_landed_api",
        fake_call_landed_api,
    )

    result = calculate_import_cost("dt 770 pro")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "landed_backend:/compare"
    assert result["data"] is not None
    assert result["data"]["tool"] == "calculate_import_cost"