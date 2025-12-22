# 配置chrome浏览器和驱动

import os
import subprocess
import win32gui
import win32con
import win32api
import time
import random

from tkinter import Tk, filedialog
from webdrivermanager_cn import ChromeDriverManagerAliMirror as ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# 启动浏览器
def start_chrome(web_address):
    # 尝试多种可能的Chrome安装路径
    chrome_paths = [
        os.path.abspath(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        os.path.abspath(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    user_data_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "chromecache")
    )
    
    # 确保用户数据目录存在
    os.makedirs(user_data_dir, exist_ok=True)
    
    # 尝试不同的Chrome路径
    chrome_path = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    
    if chrome_path is None:
        raise FileNotFoundError("找不到Chrome浏览器，请从google.cn/chrome下载安装")
    
    # 启动浏览器 - 精简参数，只保留关键防检测参数
    try:
        subprocess.Popen([
            chrome_path,
            '--remote-debugging-port=9222',
            '--no-first-run',
            '--no-default-browser-check',
            f'--user-data-dir={user_data_dir}',
            # 关键防检测参数
            '--disable-blink-features=AutomationControlled',  # 核心防检测：禁用自动化控制检测
            '--disable-extensions',                           # 禁用扩展（可能包含检测脚本）
            '--autoplay-policy=no-user-gesture-required',     # 视频自动播放：无需用户手势
            '--disable-background-timer-throttling',          # 禁用后台计时器限制（影响视频播放）
            '--disable-renderer-backgrounding',               # 禁用渲染器后台限制
            '--disable-backgrounding-occluded-windows',      # 禁用后台窗口限制
            '--disable-ipc-flooding-protection',             # 禁用IPC洪水保护
            '--disable-client-side-phishing-detection',      # 禁用客户端钓鱼检测
            '--disable-popup-blocking',                       # 禁用弹窗阻止
            '--disable-hang-monitor',                         # 禁用挂起监控
            '--disable-sync',                                 # 禁用同步
            '--disable-default-apps',                         # 禁用默认应用
            '--disable-breakpad',                             # 禁用崩溃报告
            '--disable-dev-shm-usage',                        # 禁用dev/shm使用
            '--no-sandbox',                                   # 无沙盒（提高兼容性）
            web_address    
        ])
    except Exception as e:
        print(f"启动浏览器失败: {e}")
        raise

# 启动便携式浏览器
def start_chrome_protable(web_address):
    chrome_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "chrome","App", "chrome.exe")
    )  # 设置便携版chrome浏览器的路径
    user_data_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "chromecache")
    )
    # 启动浏览器
    try:
        subprocess.Popen([
            chrome_path,
            '--remote-debugging-port=9222',     # 启用远程调试
            #'--start-maximized',               # 最大化窗口启动
            '--no-first-run',                  # 跳过首次运行向导
            '--no-default-browser-check',      # 禁用默认浏览器检查
            f'--user-data-dir={user_data_dir}',  # 设置用户数据目录
            # 关键防检测参数
            '--disable-blink-features=AutomationControlled',  # 核心防检测：禁用自动化控制检测
            '--disable-extensions',                           # 禁用扩展（可能包含检测脚本）
            '--autoplay-policy=no-user-gesture-required',     # 视频自动播放：无需用户手势
            '--disable-background-timer-throttling',          # 禁用后台计时器限制（影响视频播放）
            '--disable-renderer-backgrounding',               # 禁用渲染器后台限制
            '--disable-backgrounding-occluded-windows',       # 禁用后台窗口限制
            '--disable-ipc-flooding-protection',              # 禁用IPC洪水保护
            '--disable-client-side-phishing-detection',       # 禁用客户端钓鱼检测
            '--disable-popup-blocking',                       # 禁用弹窗阻止
            '--disable-hang-monitor',                         # 禁用挂起监控
            '--disable-sync',                                 # 禁用同步
            '--disable-default-apps',                         # 禁用默认应用
            '--disable-breakpad',                             # 禁用崩溃报告
            '--disable-dev-shm-usage',                        # 禁用dev/shm使用
            '--no-sandbox',                                   # 无沙盒（提高兼容性）
            web_address    # 默认打开的网址   
        ])
    except Exception as e:
        print(f"启动浏览器失败: {e}")
        raise FileExistsError

# 从本地获取浏览器驱动
def local_chromedriver():
    dirver_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "res", "chromedriver.exe")
    )  # 设置本地驱动路径
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # 添加防检测选项 - 移除不兼容的选项
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(executable_path=dirver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 执行脚本移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# 自动部署驱动
def auto_chromedriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  
    
    # 添加防检测选项
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = None
    try:
        # 自动安装驱动
        service = Service(ChromeDriverManager().install())
    except Exception as e:
        # 驱动安装失败时手动选择
        print(f"自动安装驱动失败：{str(e)}")
        root = Tk()
        root.withdraw()
        driver_path = filedialog.askopenfilename(title="请选择chromedriver.exe", filetypes=[("Executable files", "*.exe")])
        service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 执行脚本移除webdriver属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# 窗口布局函数
def arrange_windows(current_hwnd):
    # 等待浏览器启动
    time.sleep(2)
    # 获取屏幕尺寸
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1) 
    # 查找Chrome窗口
    def find_chrome(hwnd, extra):
        if all([
            win32gui.IsWindowVisible(hwnd),
            'chrome' in win32gui.GetWindowText(hwnd).lower(),
            win32gui.GetClassName(hwnd) == 'Chrome_WidgetWin_1',
            win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0
        ]):
            # 创建新的窗口位置元组
            placement = win32gui.GetWindowPlacement(hwnd)
            if placement[1] == win32con.SW_MAXIMIZE:
                new_placement = (placement[0],  # 元组长度
                                win32con.SW_SHOWNORMAL,  # 新的显示状态
                                placement[2],    # 最小化位置
                                placement[3],    # 最大化位置
                                placement[4])    # 正常位置
                win32gui.SetWindowPlacement(hwnd, new_placement)
            # 窗口位置调整（左半屏）
            win32gui.MoveWindow(
                hwnd,
                0,  # x位置从屏幕左侧开始
                0,  # y位置
                int(screen_width // 3*2),  # 宽度为三分之二屏
                int(screen_height*0.95),  # 高度为0.95倍屏幕高度
                True
            )
    # 当前窗口的状态设置
    current_placement = win32gui.GetWindowPlacement(current_hwnd)
    if current_placement[1] == win32con.SW_MAXIMIZE:
        new_placement = (current_placement[0],
                        win32con.SW_SHOWNORMAL,
                        current_placement[2],
                        current_placement[3],
                        current_placement[4])
        win32gui.SetWindowPlacement(current_hwnd, new_placement)
    # 遍历窗口调整Chrome窗口
    win32gui.EnumWindows(find_chrome, None)
    # 调整当前窗口到右侧半屏
    win32gui.MoveWindow(current_hwnd, int(screen_width // 3*2), 0, int(screen_width // 3), int(screen_height*0.95), True)

# 以全自动模式配置chrome
def auto_chrome(web_address):
    print("正在启动并连接浏览器")
    current_hwnd = win32gui.GetForegroundWindow()
    try:
        start_chrome(web_address)
    except Exception as e:
        print(f"启动浏览器失败: {e}")
        print("尝试使用管理员权限安装Chrome浏览器...")
        # 使用管理员权限运行winget安装命令
        import ctypes
        if ctypes.windll.shell32.IsUserAnAdmin():
            # 已经是管理员权限
            subprocess.run(["winget", "install", "Google.Chrome"])
        else:
            # 请求管理员权限
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", "cmd.exe", "/c winget install Google.Chrome", 
                None, 1
            )
        # 等待用户完成安装
        input("请在安装完成后按Enter键继续...")
        # 再次尝试启动浏览器
        try:
            start_chrome(web_address)
        except:
            print("浏览器启动失败，可能需要手动启动Chrome")
    time.sleep(2)
    arrange_windows(current_hwnd)
    driver = auto_chromedriver()
    # 关闭所有其他标签页
    handles = driver.window_handles  # 获取所有窗口句柄
    for handle in handles[1:]:      # 跳过第一个窗口
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(handles[0])  # 回到初始窗口
    print("浏览器连接成功")
    return driver

# 本地模式启动chrome
def local_chrome(web_address):
    print("正在启动并连接浏览器")
    current_hwnd = win32gui.GetForegroundWindow()
    try:
        start_chrome_protable(web_address)
    except:
        print("便携版chrome不存在,请将其置于res文件夹中")
        exit(1)
    time.sleep(2)
    arrange_windows(current_hwnd)
    try:
        driver = local_chromedriver()
    except:
        print("驱动不存在,请手动下载驱动并将chromedriver.exe置于res文件夹中")
        exit(1)
    # 关闭所有其他标签页
    handles = driver.window_handles  # 获取所有窗口句柄
    for handle in handles[1:]:      # 跳过第一个窗口
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(handles[0])  # 回到初始窗口
    print("浏览器连接成功")
    return driver

'''
if __name__ == "__main__":
    from selenium.webdriver.common.by import By
    driver = auto_chrome("https://www.sqgj.gov.cn/index")
    # driver = local_chrome("https://www.sqgj.gov.cn/index")
    print("点击测试")
    driver.find_elements(By.CLASS_NAME, "item")[2].click()'''