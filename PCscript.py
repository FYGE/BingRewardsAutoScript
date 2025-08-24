from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
import random
import GetHotSearch as GH

# 关键词列表（100个）
keywords = GH.get_weibo_hot_search_keywords_only()
#免登录操作
# 1. 找到你的 Edge 用户数据目录
# Windows 默认路径如下，将 "YourWindowsUsername" 替换为你的实际用户名
user_data_dir =r"C:\Users\gfy\AppData\Local\Microsoft\Edge\User Data"

# 2. 指定一个配置文件（Profile）
profile = "Profile001"

# 3. 配置 Edge 选项
options = webdriver.EdgeOptions()

# 关键步骤：指定用户数据目录和配置文件
# options.add_argument(f"user-data-dir={user_data_dir}")
# options.add_argument(f"profile-directory={profile}")

# 其他可选的稳定性和反检测参数
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# 如果需要无界面运行，取消注释以下行
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 启动浏览器
service = Service("msedgedriver.exe")  # 确保路径正确
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 10)
#反检测设置
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => false,
    });
    Object.defineProperty(navigator, 'plugins', {
      get: () => [1, 2, 3, 4, 5],
    });
    Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en'],
    });
    """
})

def simulate_human_scroll():
    """模拟人类的滚动行为"""
    try:
        # 获取页面高度
        page_height = driver.execute_script("return document.body.scrollHeight")
        # 随机滚动次数
        scroll_times = random.randint(3, 5)
        current_position = 0
        time.sleep(random.uniform(1, 4))
        for _ in range(scroll_times):
            # 随机滚动距离（100-500像素，适合电脑端页面）
            scroll_distance = random.randint(100, 500)
            # 30% 概率向上滚动
            if random.random() < 0.3:
                scroll_distance = -scroll_distance
            # 确保不超出页面范围
            if 0 <= current_position + scroll_distance < page_height:
                driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                current_position += scroll_distance
            else:
                # 滚动到顶部或底部
                driver.execute_script("window.scrollTo(0, arguments[0]);",
                                      0 if current_position + scroll_distance < 0 else page_height)
                break
            # 模拟人类阅读的随机停顿
            time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"滚动时发生错误: {e}")


def bing_search(query):
    try:
        driver.get("https://www.bing.com")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sb_form_q"))
        )
        search_box.clear()
        time.sleep(random.uniform(0.1, 0.2))
        search_box.send_keys(query)
        time.sleep(random.uniform(0.1, 0.2))
        search_box.send_keys(Keys.RETURN)
        # 等待搜索结果加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2 a, .b_algo a, .tilk"))
        )
        # 模拟滚动行为
        time.sleep(random.uniform(0.5, 2))
        simulate_human_scroll()
        # 额外延迟，模拟浏览时间
        time.sleep(random.uniform(4, 6))
    except Exception as e:
        print(f"搜索 {query} 时发生错误: {e}")



def StartPCBing():
    try:

        # 执行电脑端搜索
        for i in range(45):
            keyword = keywords[i]
            print(f"执行第 {i + 1} 次移动端搜索: {keyword}")
            bing_search(keyword)

        print("已完成45次电脑端搜索！")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()
