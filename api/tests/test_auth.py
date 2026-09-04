import requests
from api.services.auth import get_access_token


def test_get_access_token_success(monkeypatch):

    class MockResponse:

        def raise_for_status(self):
            pass

        def json(self):
            return {
                "access_token": "TEST_ACCESS_TOKEN"
            }

    def mock_get(url, headers, timeout):
        assert headers["Authorization"].startswith("Basic ")
        assert timeout == 10

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    token = get_access_token()

    assert token == "TEST_ACCESS_TOKEN"