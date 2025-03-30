# twitter/auth.py
# Standard library imports
import time

# Third-party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def handle_cookie_consent(driver):

    try:
        # Wait for the "Accept all cookies" button (15-second timeout)
        cookie_accept = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Accept all cookies')]"))
        )
        cookie_accept.click()
        time.sleep(2)  # Allow the page to update
        print("Accepted cookies.")
    except Exception as e:
        print(f"No cookie consent dialog found: {e}")

def handle_verification(driver, username):

    try:
        # Check for verification prompt (e.g., "Enter your username")
        prompt = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Enter your')]"))
        )
        print("Verification prompt detected. Submitting username...")

        # Find the verification input field and submit username
        verification_field = driver.find_element(By.XPATH, "//input[@name='text']")
        verification_field.send_keys(username.split("@")[0] + Keys.RETURN)  # Send username without @
        time.sleep(3)  # Wait for submission to process
        return True
    except Exception as e:
        print(f"No verification required: {e}")
        return False  # No verification needed

def login(driver, email, password, username):

    print("Navigating to Twitter login page...")
    driver.get("https://x.com/i/flow/login")

    # Step 1: Handle cookies
    handle_cookie_consent(driver)

    # Step 2: Enter email
    print("Entering email...")
    email_field = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='text']"))
    )
    email_field.send_keys(email + Keys.RETURN)
    time.sleep(3)  # Wait for next screen to load

    # Step 3: Handle verification (if triggered)
    if not handle_verification(driver, username):
        raise Exception("Verification failed. Check your username.")

    # Step 4: Enter password
    print("Entering password...")
    password_field = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))
    )
    password_field.send_keys(password + Keys.RETURN)
    time.sleep(5)  # Wait for login to complete
    print("Login successful!")