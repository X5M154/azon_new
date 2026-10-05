from mocks.stubs import ME_ENDPOINT, AuthStubs
import pytest

pytestmark = [pytest.mark.mock, pytest.mark.auth]

def test_token_goes_into_every_next_request(wiremock, mock_apis):
    auth_api, user_api = mock_apis
    wiremock.add_stub(AuthStubs.login_ok())
    wiremock.add_stub(AuthStubs.me_requires_bearer())

    auth_api.authenticate(("mock@example.com", "SuperSecret123"))
    user_api.get_user_info()

    with_token = {
        "method": "GET",
        "urlPath": ME_ENDPOINT,
        "headers": {"Authorization": {"equalTo": "Bearer mock-access-token"}},
    }
    assert wiremock.count_requests(with_token) == 1