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
tag = "여행"
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


# 게시물 더 많이 로딩하기 위한 스크롤 다운
SCROLL_PAUSE_TIME = 2

# 이미 스크롤해서 로드된 게시물 수
collected_posts = set()
scroll_count = 3  # 3번 정도 스크롤 (필요에 따라 조정)

for i in range(scroll_count):
    # 현재 게시물 수집
    posts = driver.find_elements(By.XPATH, "//a[@role='link' and contains(@href, '/p/')]")
    print(f"🔄 스크롤 {i+1}회차 - 게시물 {len(posts)}개 발견")

    for post in posts:
        href = post.get_attribute("href")
        if href and href not in collected_posts:
            collected_posts.add(href)

    # 페이지 맨 아래로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

# 결과 출력
print(f"\n✅ 총 게시물 링크 {len(collected_posts)}개 수집 완료")
for href in list(collected_posts)[:18]:  # 최대 18개 출력
    print("📌 게시물 링크:", href)

# 브라우저 종료
driver.quit()