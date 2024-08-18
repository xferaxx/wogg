from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Configuration for WebDriver
CHROME_DRIVER_PATH = 'C:/Users/PC/PycharmProjects/wog/ChromeDrive/chromedriver-win64/chromedriver.exe'
URL = 'http://127.0.0.1:5000/'


def register_user(application_url, username, password):
    """Register a new user."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Navigate to the registration page
        driver.get(application_url + 'register')

        # Find the username and password fields and enter the credentials
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the registration form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait and check if redirected to the login page
        driver.implicitly_wait(10)
        if 'login' in driver.current_url:
            print("Registration successful and redirected to login page.")
            return True
        else:
            print("Registration failed.")
            return False
    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return False
    finally:
        driver.quit()


def test_login_functionality(application_url, username, password):
    """Test the login functionality to ensure it works correctly."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Navigate to the login page
        driver.get(application_url + 'login')

        # Find the username and password fields and enter the credentials
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Press Enter to submit the form

        # Wait for the page to load and check if login was successful
        driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to load

        # Check if redirected to the homepage
        current_url = driver.current_url
        if current_url == application_url:
            print("Login successful.")
            return True
        else:
            print("Login failed.")
            return False
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False
    finally:
        driver.quit()


def test_score_after_login(application_url, username, password):
    """Test to check if the score on the index page is a number or None after login."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Navigate to the login page
        driver.get(application_url + 'login')

        # Find the username and password fields and enter the credentials
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Press Enter to submit the form

        # Wait for the page to load and check if login was successful
        driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to load

        # Check the score on the index page
        score_element = driver.find_element(By.XPATH, "//div[@class='score-container']/p/strong")
        score_text = score_element.text

        # Validate the score
        if score_text.lower() == "none":
            print("The score is None no games played yet.")
            return True
        elif score_text.isdigit():
            score = int(score_text)
            print(f"The score is a number: {score}")
            return True
        else:
            print("The score is neither a valid number nor 'None'.")
            return False
    except Exception as e:
        print(f"An error occurred during score check: {e}")
        return False
    finally:
        driver.quit()


def main_function():
    """Main function to perform registration, login, and then test the score."""
    username = 'testuser'
    password = 'testpass'

    # Register the user first
    if register_user(URL, username, password):
        print("User registration test passed.")

        # Then log in and check the score
        if test_login_functionality(URL, username, password):
            print("Login test passed.")
            if test_score_after_login(URL, username, password):
                print("Score test passed.")
            else:
                print("Score test failed.")
        else:
            print("Login test failed.")
    else:
        print("User registration test failed.")


# Run the combined test
main_function()
