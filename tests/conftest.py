import pytest
import requests

from api.api_manager import ApiManager
from config.credentials import MANAGER_INVITE, ADMIN_INVITE
from data.products import ProductData
from data.users import UserData


@pytest.fixture()
def api_manager():
    session = requests.Session()
    yield ApiManager(session)
    session.close()


@pytest.fixture()
def managers_api(registered_manager):
    session = requests.Session()
    manager = ApiManager(session)

    manager.auth_api.authenticate(
        (
            registered_manager["email"],
            registered_manager["password"]
        )
    )
    yield manager
    session.close()


@pytest.fixture
def registered_user(api_manager):
    user_data = UserData.registration_data()
    response = api_manager.auth_api.register_user(user_data)
    return {**user_data, "id": response.json()["id"]}


@pytest.fixture
def registered_manager(api_manager):
    user_data = UserData.registration_data(invite_code=MANAGER_INVITE)
    response = api_manager.auth_api.register_user(user_data)

    assert response.json()["role"] == "MANAGER"
    return {**user_data, "id": response.json()["id"]}


@pytest.fixture
def registered_admin(api_manager):
    user_data = UserData.registration_data(invite_code=ADMIN_INVITE)
    response = api_manager.auth_api.register_user(user_data)

    assert response.json()["role"] == "ADMIN"
    return {**user_data, "id": response.json()["id"]}


@pytest.fixture(scope="function")
def authenticated_user(api_manager):
    user_data = UserData.registration_data()
    register_response = api_manager.auth_api.register_user(user_data)

    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))
    return {**user_data, "id": register_response.json()["id"]}


@pytest.fixture(scope="function")
def authenticated_manager(api_manager):
    user_data = UserData.registration_data(invite_code=MANAGER_INVITE)
    register_response = api_manager.auth_api.register_user(user_data)

    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))

    me_response = api_manager.user_api.get_user_info()
    assert me_response.json()["email"] == user_data["email"]
    return {**user_data, "id": register_response.json()["id"]}


@pytest.fixture(scope="function")
def authenticated_admin(api_manager):
    user_data = UserData.registration_data(invite_code=ADMIN_INVITE)
    register_response = api_manager.auth_api.register_user(user_data)

    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))
    me_response = api_manager.user_api.get_user_info()
    assert me_response.json()["email"] == user_data["email"]
    return {**user_data, "id": register_response.json()["id"]}


@pytest.fixture
def category_id(api_manager):
    categories = api_manager.categories_api.get_categories().json()
    assert categories

    return categories[0]["id"]


@pytest.fixture
def created_product(api_manager, authenticated_admin, category_id):
    product_data = ProductData.creation_product_data(category_id)

    response = api_manager.products_api.create_product(product_data)
    product = response.json()

    yield product

    try:
        api_manager.products_api.delete_product(product["id"])
    except AssertionError:
        response = api_manager.products_api.delete_product(product["id"], expected_status=404)
        assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"