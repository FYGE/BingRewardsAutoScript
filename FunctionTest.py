from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import random

# 1. 找到你的 Edge 用户数据目录
# Windows 默认路径如下，将 "YourWindowsUsername" 替换为你的实际用户名
user_data_dir =r"C:\Users\gfy\AppData\Local\Microsoft\Edge\User Data"

# 2. 指定一个配置文件（Profile）
# 默认的配置文件是 "Default"
profile = "Profile001"

# 3. 配置 Edge 选项
options = webdriver.EdgeOptions()

# 关键步骤：指定用户数据目录和配置文件
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"profile-directory={profile}")

# 其他可选的稳定性和反检测参数
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# 你的 User-Agent 字符串
mobile_user_agent = (
    "Mozilla/5.0 (Linux; Android 14; Pixel 6 Build/AP2A.240605.024) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 Edge/121.0.2277.138"
)


options.add_argument(f"user-agent={mobile_user_agent}")

# 你还可以结合 mobileEmulation 来模拟屏幕尺寸
options.add_experimental_option("mobileEmulation", {
    "deviceMetrics": {"width": 412, "height": 732, "pixelRatio": 3.0},  # Pixel 6 尺寸
    "userAgent": mobile_user_agent
})

# 启动浏览器
service = Service("msedgedriver.exe")  # 确保路径正确
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 10)
#反检测
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
# 访问 Bing，它会以手机模式加载
driver.get("https://www.bing.com")
original_window = driver.current_window_handle
wait.until(EC.url_contains("bing.com"))
SideBar = wait.until(EC.element_to_be_clickable((By.ID, "mHamburger")))
SideBar.click()
# element_to_click = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/header/div[3]/div/div/div[2]/div[2]/div/div/div[2]/a[1]/div/div/h2"))
#     )
# element_to_click.click()
element_to_click = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//h2[text()='Rewards']"))
)
element_to_click.click()
time.sleep(random.uniform(0.3, 0.5))
driver.switch_to.window(original_window)
element = WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH, "//*[@id='HBleft']"))
    )
    # 执行点击
time.sleep(random.uniform(0.1, 0.2))
element.click()
# 保持窗口打开，观察效果
input("按回车键关闭浏览器...")

driver.quit()

