import os
import sys
import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


def make_driver(web_address):
    # 获取操作系统类型
    current_os = platform.system()
    
    # 根据操作系统选择不同的Firefox和geckodriver路径
    if current_os == "Windows":
        # Windows系统下的路径
        firefox_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "firefox.exe")
        )
        driver_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "res", "geckodriver.exe")
        )
        # 创建持久化配置文件目录
        profile_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "profile")
        )
    else:
        # Linux/macOS系统下的路径
        firefox_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "firefox")
        )
        driver_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "res", "geckodriver")
        )
        # 创建持久化配置文件目录
        profile_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "res", "firefox", "profile")
        )
    
    # 确保Firefox可执行文件存在
    if not os.path.exists(firefox_path):
        raise FileNotFoundError(f"找不到Firefox浏览器，请确保Firefox存在于 {firefox_path}")
    
    # 确保geckodriver驱动文件存在
    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"geckodriver驱动文件不存在于 {driver_path}")
    
    # 确保驱动文件有执行权限（仅Linux/macOS）
    if current_os != "Windows" and not os.access(driver_path, os.X_OK):
        os.chmod(driver_path, 0o755)
    
    # 创建Firefox选项
    firefox_options = Options()
    
    # 指定Firefox二进制文件路径
    firefox_options.binary_location = firefox_path
    
    # 使用持久化配置文件
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
       
    # 通过命令行参数指定配置文件路径
    firefox_options.add_argument(f'--profile={profile_path}')
    
    # 添加常用选项以提高兼容性
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--disable-dev-shm-usage')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-first-run')
    firefox_options.add_argument('--no-default-browser-check')

    # 设置自动播放偏好
    firefox_options.set_preference("media.autoplay.default", 0)  # 0 = 允许所有自动播放
    firefox_options.set_preference("media.autoplay.blocking_policy", 0)  # 0 = 不阻止自动播放
    firefox_options.set_preference("media.autoplay.block-event.enabled", False)  # 允许自动播放事件
    
    # 设置静音偏好
    firefox_options.set_preference("media.volume_scale", 0)  # 0 = 完全静音
    
    # 配置缓存设置 - 保留登录状态但禁用视频缓存
    # 禁用磁盘缓存
    firefox_options.set_preference("browser.cache.disk.enable", False)
    firefox_options.set_preference("browser.cache.disk.capacity", 0)
    
    # 禁用内存缓存
    firefox_options.set_preference("browser.cache.memory.enable", False)
    firefox_options.set_preference("browser.cache.memory.capacity", 0)
    
    # 禁用离线缓存
    firefox_options.set_preference("browser.cache.offline.enable", False)
    
    # 禁用媒体缓存（视频缓存）
    firefox_options.set_preference("media.cache_size", 0)
    firefox_options.set_preference("media.memory_cache_max_size", 0)
    firefox_options.set_preference("media.disk_cache_ssl", False)
    firefox_options.set_preference("media.disk_cache_non_ssl", False)
    
    # 保留Cookie和会话状态（用于登录状态）
    firefox_options.set_preference("network.cookie.lifetimePolicy", 0)  # 0 = 正常过期策略
    firefox_options.set_preference("privacy.clearOnShutdown.cookies", False)
    firefox_options.set_preference("privacy.clearOnShutdown.offlineApps", False)
    firefox_options.set_preference("privacy.clearOnShutdown.sessions", False)
    
    # 禁用预加载和预解析
    firefox_options.set_preference("network.dns.disablePrefetch", True)
    firefox_options.set_preference("network.prefetch-next", False)
    firefox_options.set_preference("network.http.speculative-parallel-limit", 0)
    
    # 禁用自动下载和保存
    firefox_options.set_preference("browser.download.useDownloadDir", False)
    firefox_options.set_preference("browser.helperApps.deleteTempFileOnExit", True)
    
    # 设置私有浏览模式（可选，但会清除登录状态）
    # firefox_options.set_preference("browser.privatebrowsing.autostart", False)  # 保持为False以保留登录状态
    
    
    # 创建服务
    service = Service(executable_path=driver_path)
    
    # 创建驱动实例
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # 打开指定网址
    driver.get(web_address)
    
    return driver

'''
if __name__ == "__main__":
    try:
        print("正在直接启动并驱动Firefox浏览器...")
        driver = make_driver("https://www.sqgj.gov.cn/index")
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
        sys.exit(1)'''