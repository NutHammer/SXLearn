
import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


def auto_chrome(web_address):
    # Firefox安装路径（当前文件向上一级目录下的res中）
    firefox_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "firefox")
    )
    
    # 确保Firefox可执行文件存在
    if not os.path.exists(firefox_path):
        raise FileNotFoundError(f"找不到Firefox浏览器，请确保Firefox存在于 {firefox_path}")
    
    # 本地geckodriver驱动路径
    driver_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "geckodriver")
    )
    
    if not os.path.exists(driver_path):
        raise FileNotFoundError("geckodriver驱动文件不存在")
    
    # 确保驱动文件有执行权限（Linux/macOS）
    if not os.access(driver_path, os.X_OK):
        os.chmod(driver_path, 0o755)
    
    # 创建Firefox选项
    firefox_options = Options()
    
    # 指定Firefox二进制文件路径
    firefox_options.binary_location = firefox_path
    
    # 添加常用选项以提高兼容性
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-first-run')
    firefox_options.add_argument('--no-default-browser-check')
    
    # 创建服务
    service = Service(executable_path=driver_path)
    
    # 创建驱动实例
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # 打开指定网址
    driver.get(web_address)
    
    return driver


def main():
    try:
        print("正在直接启动并驱动Firefox浏览器...")
        driver = auto_chrome("https://www.sqgj.gov.cn/index")
        print("Firefox浏览器已直接启动并连接成功")
        
        print("执行点击测试...")
        # 根据实际网页结构调整选择器
        elements = driver.find_elements(By.CLASS_NAME, "item")
        if len(elements) > 2:
            elements[2].click()
            print("点击操作完成")
        else:
            print("未找到足够的item元素")
            
    except Exception as e:
        print(f"程序执行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
