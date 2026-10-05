import allure
import pytest
import requests
from playwright.sync_api import expect

from api.api_manager import ApiManager
from api.auth_api import AuthAPI
from api.payment_api import PaymentAPI
from api.products_api import ProductsAPI
from api.user_api import UserAPI
from config.credentials import MANAGER_INVITE, ADMIN_INVITE
from config.hosts import MOCK_URL
from data.products import ProductData
from data.reviews import ReviewData
from data.users import UserData
from mocks.wiremock_admin import WireMockAdmin
from models.orders import OrderResponse
from models.reviews import ReviewResponse
from models.users import RegisteredUser, UserResponse
from models.products import ProductResponse
from db.db_manager import DBManager
from pages.login_page import LoginPage


@pytest.fixture
def api_manager():
    session = requests.Session()
    yield ApiManager(session)
    session.close()


@pytest.fixture
def managers_api(registered_manager):
    session = requests.Session()
    manager = ApiManager(session)

    manager.auth_api.authenticate(registered_manager.credentials)
    yield manager
    session.close()

@pytest.fixture
def admin_manager(registered_admin):
    session = requests.Session()
    admin = ApiManager(session)

    admin.auth_api.authenticate(registered_admin.credentials)
    yield admin
    session.close()

@pytest.fixture
def store_manager(registered_manager):
    session = requests.Session()
    store = ApiManager(session)

    store.auth_api.authenticate(registered_manager.credentials)
    yield store
    session.close()

@pytest.fixture
def second_user():
    session = requests.Session()
    user = ApiManager(session)
    user_data = UserData.registration_data()

    user.auth_api.register_user(user_data)
    user.auth_api.authenticate((user_data.email, user_data.password))

    yield user
    session.close()

@pytest.fixture
def registered_user(api_manager) -> RegisteredUser:
    registration = UserData.registration_data()

    response = api_manager.auth_api.register_user(registration)
    return RegisteredUser(
        registration=registration, profile=UserResponse.model_validate(response.json())
    )

@pytest.fixture
def registered_manager(api_manager):
    user_data = UserData.registration_data(invite_code=MANAGER_INVITE)
    response = api_manager.auth_api.register_user(user_data)

    assert response.json()["role"] == "MANAGER"
    return RegisteredUser(
        registration=user_data,
        profile=UserResponse.model_validate(response.json()),
    )


@pytest.fixture
def registered_admin(api_manager):
    user_data = UserData.registration_data(invite_code=ADMIN_INVITE)
    response = api_manager.auth_api.register_user(user_data)

    assert response.json()["role"] == "ADMIN"
    return RegisteredUser(
        registration=user_data,
        profile=UserResponse.model_validate(response.json()),
    )


@pytest.fixture(scope="function")
def authenticated_user(api_manager, registered_user):

    api_manager.auth_api.authenticate(registered_user.credentials)
    return registered_user


@pytest.fixture(scope="function")
def authenticated_manager(api_manager, registered_manager):

    api_manager.auth_api.authenticate(registered_manager.credentials)

    me_response = api_manager.user_api.get_user_info()
    assert me_response.json()["email"] == registered_manager.registration.email
    return registered_manager


@pytest.fixture(scope="function")
def authenticated_admin(api_manager, registered_admin):

    api_manager.auth_api.authenticate(registered_admin.credentials)
    me_response = api_manager.user_api.get_user_info()
    assert me_response.json()["email"] == registered_admin.registration.email
    return registered_admin


@pytest.fixture
def category_id(api_manager):
    categories = api_manager.categories_api.get_categories().json()
    assert categories

    return categories[0]["id"]


@pytest.fixture
def created_product(admin_manager, category_id):
    product_data = ProductData.creation_product_data(category_id)

    response = admin_manager.products_api.create_product(product_data)
    product = ProductResponse.model_validate(response.json())

    yield product

    try:
        admin_manager.products_api.delete_product(product.id)
    except AssertionError:
        response = admin_manager.products_api.delete_product(product.id, expected_status=404)
        assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"

@pytest.fixture
def created_order(api_manager, authenticated_user, created_product):

    api_manager.cart_api.add_item(ProductData.cart_item_data(created_product.id))

    response = api_manager.payment_api.checkout()
    assert response.json()["status"] == "AWAITING_PAYMENT"

    order = OrderResponse.model_validate(response.json())

    yield order

    new_response = api_manager.payment_api.get_order(order.id)
    new_order = OrderResponse.model_validate(new_response.json())

    if new_order.status == "AWAITING_PAYMENT":
        api_manager.payment_api.cancel_order(order.id)

@pytest.fixture
def created_review(api_manager, authenticated_user, created_product):
    review_data = ReviewData.creation_review_data()

    response = api_manager.reviews_api.create_review(created_product.id, review_data)

    return ReviewResponse.model_validate(response.json())

@pytest.fixture(scope="session")
def db():
    """Соединения с базами стенда - по одному на весь прогон."""

    manager = DBManager()
    yield manager
    manager.close()

@pytest.fixture
def wiremock():
    """Чистый WireMock перед каждым тестом: свои стабы, свой журнал запросов."""
    admin = WireMockAdmin()

    if not admin.is_running():
        pytest.skip(f"WireMock не отвечает на {MOCK_URL} - тесты с моками пропускаем")

    admin.reset()
    yield admin
    admin.session.close()

@pytest.fixture
def mock_apis(wiremock):
    session = requests.Session()
    yield AuthAPI(session, base_url=MOCK_URL), UserAPI(session, base_url=MOCK_URL)
    session.close()

@pytest.fixture
def mock_products_api(wiremock):
    """Наш обычный ProductsAPI, только смотрит он не на стенд, а в мок."""
    session = requests.Session()
    yield ProductsAPI(session, base_url=MOCK_URL)
    session.close()

@pytest.fixture
def mock_payment_api(wiremock):
    session = requests.Session()
    yield PaymentAPI(session, base_url=MOCK_URL)
    session.close()

@pytest.fixture
def mobile_page(browser, playwright):
    """Тот же браузер, но притворяется телефоном: размер экрана, User-Agent, касания."""
    context = browser.new_context(**playwright.devices["iPhone 13"])
    page = context.new_page()

    yield page

    context.close()

@pytest.fixture
def ui_user(api_manager):

    registration = UserData.registration_data()

    api_manager.auth_api.register_user(registration)

    return registration

def _login_through_ui(page, user):
    """Вход через форму: одинаковый и для десктопа, и для телефона."""
    login_page = LoginPage(page).open()
    login_page.login(user.email, user.password)

    expect(login_page.profile_link).to_have_text(user.email)
    return page

@pytest.fixture
def logged_in_page(page, ui_user):
    """Вкладка браузера, в которой мы уже вошли в свой аккаунт."""
    return _login_through_ui(page, ui_user)

@pytest.fixture
def logged_in_mobile_page(mobile_page, ui_user):
    return _login_through_ui(mobile_page, ui_user)

'''
@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright):
    """На проекте атрибут называется data-qa - учим get_by_test_id искать именно его."""
    playwright.selectors.set_test_id_attribute("data-qa")
'''

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Упал тест в браузере - кладём в отчёт скриншот и адрес страницы."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    # у API-тестов страницы нет, у мобильных она называется иначе
    page = item.funcargs.get("mobile_page") or item.funcargs.get("page")
    if page is None:
        return

    allure.attach(
        page.screenshot(full_page=True),
        name="Скриншот в момент падения",
        attachment_type=allure.attachment_type.PNG,
    )
    allure.attach(page.url, name="Адрес страницы", attachment_type=allure.attachment_type.TEXT)