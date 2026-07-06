from packages.tools.product.get_product_details_tool import get_product_details
from packages.tools.product.search_products_tool import search_products


def test_search_products_returns_normalized_dict(monkeypatch):
    def fake_call_landed_api(path, params=None, trace_id=None):
        return {
            "ok": True,
            "trace_id": trace_id,
            "source": "landed_api",
            "data": {
                "products": [
                    {
                        "product_id": "dt770-pro",
                        "name": "Beyerdynamic DT 770 Pro",
                    }
                ]
            },
        }

    monkeypatch.setattr(
        "packages.tools.product.search_products_tool.call_landed_api",
        fake_call_landed_api,
    )

    result = search_products("dt 770 pro")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "landed_backend:/search"
    assert result["data"] is not None
    assert result["data"]["tool"] == "search_products"


def test_get_product_details_returns_normalized_dict(monkeypatch):
    def fake_call_landed_api(path, params=None, trace_id=None):
        return {
            "ok": True,
            "trace_id": trace_id,
            "source": "landed_api",
            "data": {
                "product": {
                    "product_id": "dt770-pro",
                    "name": "Beyerdynamic DT 770 Pro",
                }
            },
        }

    monkeypatch.setattr(
        "packages.tools.product.get_product_details_tool.call_landed_api",
        fake_call_landed_api,
    )

    result = get_product_details("dt 770 pro")

    assert result["ok"] is True
    assert result["trace_id"]
    assert result["source"] == "landed_backend:/products/resolve/preview"
    assert result["data"] is not None
    assert result["data"]["tool"] == "get_product_details"