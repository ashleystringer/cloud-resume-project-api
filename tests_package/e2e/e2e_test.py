import pytest
from playwright.sync_api import Playwright, APIRequestContext
import os
from typing import Generator

##api_url = "https://{API_ID}.execute-api.{AWS_REGION}.amazonaws.com/count"
api_url = os.environ.get("API_URL") + '/count'

@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    '''
    request_context = playwright.request.new_context(
        base_url="https://{API_ID}.execute-api.{AWS_REGION}.amazonaws.com"
    )
    '''
    
    request_context = playwright.request.new_context(
        base_url = api_url
    )

    yield request_context
    request_context.dispose()


def test_get_request(api_request_context: APIRequestContext) -> None:
    print("this is test_get_request")
    response = api_request_context.get(api_url)
    assert response.ok
    assert response.status == 200
    assert response.headers["content-type"] == "application/json"
    print(response)
    assert response.json() == {'count': 0, 'msg': 'GET /count reached'}

def test_put_request(api_request_context: APIRequestContext) -> None:
    print("this is test_put_request")
    response = api_request_context.put(api_url)
    assert response.ok
    assert response.status == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {'count': 1, 'msg': 'PUT /count reached'}