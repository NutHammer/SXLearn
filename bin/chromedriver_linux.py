# 配置chrome浏览器和驱动 - Linux版本（UOS优化）

import os
import subprocess
import time
import socket
import sys

from webdrivermanager_cn import ChromeDriverManagerAliMirror as ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException


# 检查端口是否可连接
def check_port_available(host='127.0.0.1', port=9222, timeout=30):
    """检查端口是否可连接"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                print(f"端口 {port} 已就绪")
                return True
        except:
            pass
        time.sleep(1)
    print(f"端口 {port} 连接超时")
    return False


# 检查是否已有Chrome进程在运行
def check_existing_chrome():
    """检查是否已有Chrome进程在运行"""
    try:
        # 检查9222端口是否已被占用
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 9222))
        sock.close()
        if result == 0:
            print("检测到已有Chrome进程在运行，尝试连接...")
            return True
    except:
        pass
    
    # 检查Chrome进程是否存在
    try:
        result = subprocess.run(['pgrep', '-f', 'chrome'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("检测到Chrome进程正在运行")
            return True
    except:
        pass
    
    return False


# 启动浏览器（简化版本）
def start_chrome(web_address):
    # UOS系统特定的Chrome路径
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/opt/google/chrome/chrome",
        "/opt/google/chrome/google-chrome",
        os.path.expanduser("~/.local/share/flatpak/exports/bin/com.google.Chrome")
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
        # 尝试通过which命令查找
        try:
            which_result = subprocess.run(["which", "google-chrome"], capture_output=True, text=True)
            if which_result.returncode == 0:
                chrome_path = which_result.stdout.strip()
        except:
            pass
    
    if chrome_path is None:
        raise FileNotFoundError("找不到Chrome浏览器，请安装Google Chrome或Chromium")
    
    print(f"使用Chrome路径: {chrome_path}")
    
    # 先检查是否已有Chrome进程在运行
    if check_existing_chrome():
        print("使用现有Chrome进程")
        return None
    
    # 使用最简单的启动方式，模仿手动命令
    chrome_args = [
        chrome_path,
        '--remote-debugging-port=9222',
        '--remote-debugging-address=0.0.0.0',
        f'--user-data-dir={user_data_dir}',
        '--no-first-run',
        '--no-default-browser-check',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        web_address
    ]
    
    print(f"启动命令: {' '.join(chrome_args)}")
    
    # 使用最简单的启动方式
    try:
        # 方法1：直接使用subprocess.Popen，不重定向输出
        print("方法1：直接启动Chrome...")
        process = subprocess.Popen(
            chrome_args,
            env=os.environ.copy()  # 使用当前环境变量
        )
        
        # 等待启动
        time.sleep(5)
        
        # 检查进程状态
        if process.poll() is not None:
            print("方法1失败，尝试方法2...")
            # 方法1失败，尝试方法2：使用shell命令
            shell_cmd = f"{chrome_path} --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --user-data-dir={user_data_dir} --no-first-run --no-default-browser-check --no-sandbox --disable-dev-shm-usage {web_address} &"
            process = subprocess.Popen(shell_cmd, shell=True)
            time.sleep(5)
            
            if process.poll() is not None:
                print("方法2失败，尝试方法3...")
                # 方法3：使用nohup在后台启动
                nohup_cmd = f"nohup {chrome_path} --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --user-data-dir={user_data_dir} --no-first-run --no-default-browser-check --no-sandbox --disable-dev-shm-usage {web_address} > /dev/null 2>&1 &"
                process = subprocess.Popen(nohup_cmd, shell=True)
                time.sleep(5)
        
        # 最终检查端口是否可用
        if check_port_available(timeout=10):
            print("Chrome启动成功")
            return process
        else:
            raise Exception("Chrome启动后端口不可用")
            
    except Exception as e:
        print(f"启动浏览器失败: {e}")
        # 尝试最后的方法：使用系统调用
        try:
            print("尝试最后的方法：使用os.system...")
            system_cmd = f"{chrome_path} --remote-debugging-port=9222 --user-data-dir={user_data_dir} --no-sandbox {web_address} &"
            os.system(system_cmd)
            time.sleep(5)
            
            if check_port_available(timeout=10):
                print("Chrome启动成功（系统调用）")
                return True
            else:
                raise Exception("系统调用启动失败")
        except Exception as e2:
            print(f"所有启动方法都失败: {e2}")
            raise


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
        # UOS环境下不使用图形界面选择，直接提示手动安装
        print(f"自动安装驱动失败：{str(e)}")
        print("请手动安装ChromeDriver：")
        print("1. 访问 https://chromedriver.chromium.org/ 下载对应版本的ChromeDriver")
        print("2. 解压后将chromedriver文件放到系统PATH中或当前目录")
        print("3. UOS系统可使用命令安装：sudo apt install chromium-chromedriver")
        return None
    
    # 尝试连接，最多重试5次
    max_retries = 5
    for attempt in range(max_retries):
        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            # 执行脚本移除webdriver属性
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print(f"WebDriver连接成功 (第{attempt + 1}次尝试)")
            return driver
        except WebDriverException as e:
            error_msg = str(e)
            print(f"WebDriver连接失败 ({attempt + 1}/{max_retries}): {error_msg}")
            
            if "connection refused" in error_msg.lower():
                print("连接被拒绝，可能是Chrome未启动或端口不可用")
            elif "invalid argument" in error_msg.lower():
                print("参数无效，检查ChromeDriver版本")
            elif "unknown error" in error_msg.lower():
                print("未知错误，可能是网络或权限问题")
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 3  # 递增等待时间
                print(f"等待{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print("达到最大重试次数，连接失败")
                raise


# 以全自动模式配置chrome
def auto_chrome(web_address):
    print("正在启动并连接浏览器")
    
    # 先检查端口是否可用
    if not check_port_available(timeout=5):
        print("启动新的Chrome实例...")
        try:
            chrome_process = start_chrome(web_address)
            if chrome_process is None:
                print("使用现有Chrome进程")
        except Exception as e:
            print(f"启动浏览器失败: {e}")
            print("请检查：")
            print("1. Chrome浏览器是否已正确安装")
            print("2. 尝试手动启动: google-chrome --remote-debugging-port=9222")
            print("3. 检查是否有其他Chrome进程占用9222端口")
            return None
    else:
        print("使用现有Chrome进程")
    
    # 等待浏览器完全启动
    print("等待浏览器启动完成...")
    if not check_port_available(timeout=15):
        print("浏览器启动超时，但尝试强制连接...")
    
    try:
        driver = auto_chromedriver()
        if driver is None:
            return None
            
        # 关闭所有其他标签页
        handles = driver.window_handles
        if len(handles) > 1:
            for handle in handles[1:]:
                driver.switch_to.window(handle)
                driver.close()
            driver.switch_to.window(handles[0])
            
        print("浏览器连接成功")
        return driver
    except Exception as e:
        print(f"浏览器连接失败: {e}")
        # 提供详细的调试信息
        print("\n调试建议：")
        print("1. 手动运行: google-chrome --remote-debugging-port=9222")
        print("2. 在另一个终端运行: curl http://127.0.0.1:9222/json")
        print("3. 检查ChromeDriver版本是否匹配Chrome版本")
        print("4. 检查是否有防火墙或权限限制")
        return None


# 清理函数
def cleanup_chrome():
    """清理Chrome进程"""
    try:
        # 杀死Chrome相关进程
        subprocess.run(['pkill', '-f', 'chrome'], capture_output=True)
        print("已清理Chrome进程")
    except:
        pass


'''
if __name__ == "__main__":
    try:
        from selenium.webdriver.common.by import By
        driver = auto_chrome("https://www.sqgj.gov.cn/index")
        if driver:
            print("点击测试")
            driver.find_elements(By.CLASS_NAME, "item")[2].click()
    finally:
        cleanup_chrome()
'''