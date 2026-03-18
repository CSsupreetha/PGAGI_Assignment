import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
INVALID_USER = "invalid_user"
PASSWORD = "secret_sauce"
INVALID_PASSWORD = "wrongpassword"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def login(driver, username, password):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


# TC01: Login with valid credentials
def test_valid_login(driver):
    login(driver, VALID_USER, PASSWORD)
    assert "inventory" in driver.current_url, "Expected to land on inventory page after valid login"
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"


# TC02: Login with invalid credentials
def test_invalid_login(driver):
    login(driver, INVALID_USER, INVALID_PASSWORD)
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed(), "Error message should be displayed for invalid login"
    assert "Username and password do not match" in error.text


# TC03: Product listing validation
def test_product_listing(driver):
    login(driver, VALID_USER, PASSWORD)
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) > 0, "No products found on the listing page"

    for product in products:
        name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
        price = product.find_element(By.CLASS_NAME, "inventory_item_price").text
        button = product.find_element(By.CLASS_NAME, "btn_inventory")

        assert name != "", f"Product name is empty"
        assert "$" in price, f"Product price '{price}' does not contain '$'"
        assert button.is_displayed(), f"Add to cart button not visible for {name}"


# TC04: Add product(s) to cart
def test_add_to_cart(driver):
    login(driver, VALID_USER, PASSWORD)

    add_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    add_buttons[0].click()

    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1", f"Cart badge should show 1, but shows {cart_badge.text}"

    add_buttons[1].click()
    assert cart_badge.text == "2", f"Cart badge should show 2, but shows {cart_badge.text}"


# TC05: Cart content validation
def test_cart_contents(driver):
    login(driver, VALID_USER, PASSWORD)

    first_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    first_product_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert "cart" in driver.current_url

    cart_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    cart_item_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

    assert cart_item_name == first_product_name, "Product name in cart does not match"
    assert cart_item_price == first_product_price, "Product price in cart does not match"


# TC06: Checkout flow (happy path)
def test_checkout_flow(driver):
    login(driver, VALID_USER, PASSWORD)

    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    assert "checkout-step-one" in driver.current_url

    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("560001")
    driver.find_element(By.ID, "continue").click()

    assert "checkout-step-two" in driver.current_url
    assert driver.find_element(By.CLASS_NAME, "summary_info").is_displayed()

    driver.find_element(By.ID, "finish").click()
    assert "checkout-complete" in driver.current_url

    confirmation = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "Thank you" in confirmation, f"Expected thank you message, got: {confirmation}"


# TC07: Logout
def test_logout(driver):
    login(driver, VALID_USER, PASSWORD)

    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(0.5)
    driver.find_element(By.ID, "logout_sidebar_link").click()

    assert driver.current_url == BASE_URL + "/", "Should redirect to login page after logout"
    assert driver.find_element(By.ID, "login-button").is_displayed()