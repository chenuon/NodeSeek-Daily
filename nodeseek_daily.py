import undetected_chromedriver as uc
import time
import random
import os
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取系统中 Chrome 的版本
def get_chrome_version():
    try:
        result = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        version = result.split()[2]  # 提取版本号，如 "134.0.6998.0"
        major_version = version.split('.')[0]  # 提取主版本号，如 "134"
        return major_version
    except Exception as e:
        print(f"无法获取 Chrome 版本: {e}")
        return None

def setup_driver_and_cookies():
    print("开始初始化浏览器...")
    print("启用无头模式...")
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 获取 Chrome 版本并设置 ChromeDriver 目标版本
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"检测到 Chrome 版本: {chrome_version}")
        uc.TARGET_VERSION = int(chrome_version)  # 设置匹配的 ChromeDriver 版本

    try:
        print("正在启动Chrome...")
        driver = uc.Chrome(options=options)
        driver.get('https://www.nodeseek.com/sign')
        cookies = [
            {'name': 'username', 'value': os.getenv('USERNAME')},
            {'name': 'password', 'value': os.getenv('PASSWORD')}
        ]
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        return driver
    except Exception as e:
        print(f"设置浏览器和Cookie时出错: {e}")
        raise

def post_comment(driver):
    print("开始执行评论操作...")
    driver.get('https://www.nodeseek.com/board')
    time.sleep(random.uniform(2, 5))
    
    try:
        post_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/post/"]'))
        )
        post_link.click()
        time.sleep(random.uniform(2, 5))
        
        comment_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'reply_content'))
        )
        comments = [
            "感谢分享，很有帮助！",
            "不错的内容，支持一下！",
            "学习了，谢谢楼主！",
            "这个帖子很有意思！",
            "赞一个，继续加油！"
        ]
        comment_box.send_keys(random.choice(comments))
        time.sleep(random.uniform(1, 3))
        
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()
        print("评论成功！")
        time.sleep(random.uniform(2, 5))
    except Exception as e:
        print(f"评论操作失败: {e}")

def main():
    print("开始执行NodeSeek评论脚本...")
    driver = None
    try:
        driver = setup_driver_and_cookies()
        post_comment(driver)
    except Exception as e:
        print(f"脚本执行失败: {e}")
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭，脚本执行完毕。")

if __name__ == "__main__":
    main()
