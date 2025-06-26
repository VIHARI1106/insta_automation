from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Instagram credentials
username = "Dmorgan_123"
password = "Dexter@123"
profile_url = "https://www.instagram.com/cbitosc/"

# Launch browser
driver = webdriver.Chrome()
driver.maximize_window()

# Step 1: Login
driver.get("https://www.instagram.com/accounts/login/")
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password + "\n")
print("✅ Logged in")
time.sleep(5)

# Step 2: Close popups
for _ in range(2):
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
        ).click()
        print("✅ Dismissed popup")
    except:
        pass
    time.sleep(1)

# Step 3: Open profile directly
driver.get(profile_url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
print("🔗 Profile loaded")
time.sleep(3)

# Step 4: Follow if not already
try:
    follow_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Follow']"))
    )
    follow_button.click()
    print("✅ Followed the account")
    time.sleep(2)
except:
    print("⚠️ Already following or no follow button")

# Step 5: Extract and parse meta tag
try:
    meta_desc = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute("content")
    print("🔍 DEBUG META:", meta_desc)

    # Extract followers, following, posts
    stat_match = re.search(r"([\d,]+)\s+Followers,\s+([\d,]+)\s+Following,\s+([\d,]+)\s+Posts", meta_desc)
    followers = stat_match.group(1) if stat_match else "Not found"
    following = stat_match.group(2) if stat_match else "Not found"
    posts = stat_match.group(3) if stat_match else "Not found"

    # Extract name and username
    name_match = re.search(r"- (.*?) \(@(.*?)\)", meta_desc)
    name = name_match.group(1) if name_match else "Not found"
    username_extracted = name_match.group(2) if name_match else "Not found"

    # Extract bio from quotes
    bio_match = re.search(r':\s*"(.+?)"', meta_desc)
    bio = bio_match.group(1) if bio_match else "Not found"

except Exception as e:
    print("❌ Failed to parse meta:", e)
    followers = following = posts = name = username_extracted = bio = "Not found"

# Step 6: Save data to file
with open("cbitosc_info.txt", "w", encoding="utf-8") as f:
    f.write(f"Community Name: {name}\n")
    f.write(f"Username: @{username_extracted}\n")
    f.write(f"Bio: {bio}\n")
    f.write(f"Posts: {posts}\n")
    f.write(f"Followers: {followers}\n")
    f.write(f"Following: {following}\n")

print("📌 Community Name:", name)
print("📌 Username: @" + username_extracted)
print("📌 Bio:", bio)
print(f"📌 Posts: {posts} | Followers: {followers} | Following: {following}")
print("✅ Data written to cbitosc_info.txt")
driver.quit()
