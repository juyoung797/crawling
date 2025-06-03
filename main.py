from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO

# .env 파일 로드
load_dotenv()

# 환경변수 읽기
insta_id = os.getenv("INSTA_ID")
insta_pw = os.getenv("INSTA_PW")

# 브라우저 드라이버 설정 및 창 크기 조정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
act = ActionChains(driver)

# 인스타그램 로그인 페이지 접속
driver.get("https://www.instagram.com/accounts/login/")
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "username")))

# 로그인 정보 입력
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(insta_id)  # 본인 인스타그램 ID
password_input.send_keys(insta_pw)  # 본인 비밀번호
password_input.send_keys(Keys.ENTER)

time.sleep(5)

# 버튼 목록 확인
buttons = driver.find_elements(By.TAG_NAME, "button")
print("🔍 현재 페이지 버튼 목록:")
for btn in buttons:
    try:
        print("-", btn.text)
    except:
        pass


# '나중에 하기' 버튼 클릭
try:
    not_now_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), '나중에 하기')]")))
    not_now_button.click()
    print("🔔 '나중에 하기' 버튼 클릭 완료")
except Exception as e:
    print("❌ '나중에 하기' 버튼을 찾을 수 없습니다:", e)

# 해시태그 페이지 접속
tag = "대형카페"
driver.get(f"https://www.instagram.com/explore/tags/{tag}/")
time.sleep(5)

# # 게시물 링크 수집
# try:
#     post_links = WebDriverWait(driver, 15).until(
#         EC.presence_of_all_elements_located((By.XPATH, "//a[@role='link' and contains(@href, '/p/')]"))
#     )
#     print(f"✅ 게시물 {len(post_links)}개 발견")
#     for link in post_links[:5]:
#         print("📌 게시물 링크:", link.get_attribute('href'))
# except Exception as e:
#     print("❌ 게시물 링크를 찾을 수 없습니다:", e)


# 게시물 더 많이 로딩하기 위한 스크롤 다운 타임
SCROLL_PAUSE_TIME = 2

# 이미 스크롤해서 로드된 게시물 수
posts = list()
collected_posts = set()
scroll_count = 10  # 스크롤횟수 (필요에 따라 조정)

for i in range(1, scroll_count):
    # 현재 게시물 수집
    posts = driver.find_elements(By.XPATH, "//a[@role='link' and contains(@href, '/p/')]")
    print(f"🔄 스크롤 {i}회차 - 게시물 {len(posts)}개 발견")
    for post in posts:
        href = post.get_attribute("href")
        if href and href not in collected_posts:
            collected_posts.add(href)

    # 페이지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

# 결과 출력
print(f"\n✅ 총 게시물 링크 {len(collected_posts)}개 수집 완료")
for href in list(collected_posts)[:50]:  # 최대 18개 출력
    print("📌 게시물 링크:", href)

import os

# 저장 경로 지정 (dataset/images 폴더 아래)
save_dir = "./dataset/images"
os.makedirs(save_dir, exist_ok=True)  # 폴더 없으면 생성

saved_url_file = os.path.join(save_dir, "saved_image_urls.txt")
saved_urls = set()

if os.path.exists(saved_url_file):
    with open(saved_url_file, "r") as f:
        saved_urls = set(line.strip() for line in f if line.strip())

print(f"📂 이전에 저장된 이미지 URL 수: {len(saved_urls)}")

image_urls = []

for i, post_url in enumerate(list(collected_posts)[:len(collected_posts)]):
    try:
        driver.get(post_url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'x5yr21d')]"))
        )
        img_elem = driver.find_element(By.XPATH, "//img[contains(@class, 'x5yr21d')]")
        img_url = img_elem.get_attribute("src")

        if img_url:
            if img_url in saved_urls:
                print(f"🔁 {i+1}번째 이미지 URL은 이미 저장됨. 스킵")
            else:
                image_urls.append(img_url)
                saved_urls.add(img_url)
                print(f"🆕 {i+1}번째 새 이미지 URL:", img_url)
        else:
            print(f"⚠️ {i+1}번째 게시물에서 이미지 URL 없음")

        time.sleep(1)

    except Exception as e:
        print(f"❌ {i+1}번째 게시물 이미지 추출 실패:", e)

# 새로 수집한 URL 파일에 추가 저장
with open(saved_url_file, "a") as f:
    for url in image_urls:
        f.write(url + "\n")

print(f"\n✅ 총 {len(image_urls)}개의 새 이미지 URL 저장 완료")


# 이미지 링크로부터 이미지 다운로드
save_dir = "dataset/images/train"
os.makedirs(save_dir, exist_ok=True)

for idx, url in enumerate(image_urls):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img_path = os.path.join(save_dir, f"ins_{idx:04}.jpg")
        img.save(img_path)
        print(f"✅ 저장 완료: {img_path}")
    except Exception as e:
        print(f"❌ 저장 실패: {url}", e)

# 브라우저 종료
driver.quit()