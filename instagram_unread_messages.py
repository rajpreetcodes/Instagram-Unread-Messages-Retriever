from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Set up the webdriver (you'll need to specify the path to your chromedriver)
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

# Navigate to the login page
driver.get('https://www.instagram.com/')

try:
    # Wait for the username field to be visible
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    
    # Enter username
    username_field.send_keys('YOUR USERNAME HERE')  # Type your username here
    
    # Find and fill the password field
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('YOUR PASSWORD HERE')  # Type your password here
    
    # Find and click the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))  # Locate the login button
    )
    login_button.click()
    
    # Wait for successful login (e.g., by checking for an element on the next page)
    print("Login successful!")

    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-spinner"))
    )

    # Open Instagram Direct Messaging
    messages_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Messenger']"))
    )
    messages_button.click()

    # Bypass the turn on notifications prompt
    not_now_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Not Now')]"))  # Locate the login button
    )
    not_now_button.click()

    # Wait until the messages load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='listitem']"))
    )

    messages = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem']")

    unread_messages = []
    for message in messages:
        try:
            # Check if the message has a blue background (unread)
            if "x1n2onr6" in message.get_attribute("class"):  # Replace with actual class for unread messages
                # Get sender name
                sender = message.find_element(By.CSS_SELECTOR, "span[dir='auto']").text

                # Get message content (the preview text shown in the list)
                message_content = message.find_element(By.CSS_SELECTOR, "div > div > div:nth-child(2)").text

                # Get timestamp if available
                try:
                    timestamp = message.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
                except:
                    timestamp = "Time not available"

                unread_messages.append({
                    "sender": sender,
                    "content": message_content,
                    "time": timestamp
                })
        except Exception as e:
            print(f"Error processing message: {e}")

    # Print unread messages with content
    print("\nUnread Messages:")
    for msg in unread_messages:
        print(f"From: {msg['sender']}")
        print(f"Message: {msg['content']}")
        print("-" * 50)

# Remove or comment out this line to keep the browser open
finally:
    driver.quit()
