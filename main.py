from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
options.add_argument(f"--user-data-dir={user_data_dir}")

class Instafollower:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.instagram.com")

    def find_followers(self):
        wait = WebDriverWait(self.driver, 20)

        # Open profile
        profile_link = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a[role='link'] div")))
        profile_link.click()

        # Open followers list
        followers_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]")))
        followers_btn.click()

    def follow(self, scroll_pause=2, max_scrolls=10):
        wait = WebDriverWait(self.driver, 20)

        # Wait until dialog with followers is visible
        dialog = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "div[role='dialog']")))

        for _ in range(max_scrolls):
            # Find all follow buttons
            buttons = dialog.find_elements(By.XPATH, ".//button[normalize-space()='Follow']")

            for btn in buttons:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(btn))
                    if btn.text.strip().lower() == "follow":
                        time.sleep(0.5)
                        btn.click()
                        time.sleep(1)  # short pause between clicks

                except ElementClickInterceptedException:
                    try:
                        popup_button = WebDriverWait(self.driver, 3).until(
                            ec.element_to_be_clickable((By.XPATH,
                                                        "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/button[2]"))
                        )
                        popup_button.click()

                    except Exception as e:
                        print(f"Error: {e}")
                except Exception:
                    print(f"Skipped a button")

            # scroll the dialog further to load more users
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
            time.sleep(scroll_pause)


insta = Instafollower()
time.sleep(3)
insta.find_followers()
time.sleep(3)
insta.follow(scroll_pause=3, max_scrolls=20)

