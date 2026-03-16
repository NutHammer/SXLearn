#  程序入口、初始化、交互界面V1.1
import threading
import time
import tkinter as tk
from tkinter import ttk

import browser_driver
from base_learn import BaseLearn
from ui_handlers import UIHandlers

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("启动中...")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # 居中显示
        self.center_window()
        
        # 设置窗口样式
        self.root.configure(bg='#f0f0f0')
        
        # 添加标签
        label = tk.Label(
            self.root, 
            text="正在启动浏览器...\n请稍候...", 
            font=("微软雅黑", 12),
            bg='#f0f0f0',
            fg='#333333'
        )
        label.pack(expand=True)
        
        # 添加进度条
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(pady=10)
        
        # 启动动画
        self.progress.start(10)
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def destroy(self):
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.after(0, self.root.destroy)

def run_selected_script():
    web_address = "https://www.sqgj.gov.cn/index"
    driver = None
    
    # 创建启动画面
    splash = SplashScreen()
    
    # 在后台线程中启动浏览器
    def start_browser():
        nonlocal driver
        try:
            driver = browser_driver.make_driver(web_address)
        except Exception as e:
            print(f"浏览器启动失败: {e}")
        finally:
            # 关闭启动画面
            splash.root.after(0, splash.destroy)
    
    # 启动浏览器线程
    browser_thread = threading.Thread(target=start_browser, daemon=True)
    browser_thread.start()
    
    # 显示启动画面
    try:
        splash.show()
        splash.root.mainloop()
    except tk.TclError:
        # 如果窗口已被销毁，则继续
        pass
    
    # 等待浏览器启动完成
    browser_thread.join()
    
    if driver is None:
        print("无法启动浏览器，程序退出")
        return
    
    # 初始化UI处理器
    ui_handler = UIHandlers(driver)
        
    # 显示欢迎信息
    ui_handler.print_to_window("陕西干部网络学院刷课工具")
    
    # 设置浏览器关闭监听器
    def check_browser_closed():
        try:
            # 尝试访问浏览器窗口，如果已关闭则会抛出异常
            driver.current_url
            # 如果能访问到URL，继续每秒检查一次
            import threading
            t = threading.Timer(0.5, check_browser_closed)
            t.daemon = True
            t.start()
        except:
            # 浏览器已关闭，退出程序
            driver.quit()
            import os
            os._exit(0)  # 强制退出程序
    
    # 开始监听浏览器关闭
    check_browser_closed()
        
    while True:
        # 显示菜单选项
        # menu_message = "="*25 + "\n"
        menu_message =  "\n输入 0 完成网络自学\n"
        menu_message += "输入 整数n 完成第n个专题学习\n"
        menu_message += "输入 A 学习全部课程\n"
        menu_message += "输入 Q 退出程序"
        ui_handler.print_to_window(menu_message)
        
        # 显示输入框并获取用户输入
        try:
            choice = ui_handler.input_from_window("\n请登录并选课后输入功能编号：")
        except:
            break
        
        # 处理用户输入
        if choice and choice.lower() == 'q':
            ui_handler.print_to_window("程序退出")
            break
        elif choice and choice.lower() == 'a':
            ui_handler.print_to_window("开始学习所有课程...")
            for i in range(10):
                try:
                    if i == 0:
                        ui_handler.print_to_window("开始完成网络自学...")
                    else:
                        ui_handler.print_to_window(f"开始学习第{i}个专题...")
                    learner = BaseLearn(driver, ui_handler=ui_handler)
                    learner.run_learning_cycle(button_index=i)
                except Exception as e:
                    ui_handler.print_to_window(f"\n专题 {i} 已学完或发生错误: {str(e)}")
                    ui_handler.print_to_window("继续执行下一个专题...")
        else:
            try:
                if choice:
                    choice = int(choice)
                    if 0 <= choice <= 9:
                        if choice == 0:
                            ui_handler.print_to_window("开始完成网络自学...")
                        else:
                            ui_handler.print_to_window(f"开始学习第{choice}个专题...")
                        learner = BaseLearn(driver, ui_handler=ui_handler)
                        learner.run_learning_cycle(button_index=choice)
                    else:
                        ui_handler.print_to_window("请输入0-9之间的整数")
                else:
                    ui_handler.print_to_window("请输入有效的整数（0-9）或A（执行所有选项）")
            except ValueError:
                ui_handler.print_to_window("请输入有效的整数（0-9）或A（执行所有选项）")

    # 程序正常退出时关闭浏览器
    if driver:
        driver.quit()
        print("浏览器已关闭")


if __name__ == "__main__":
    run_selected_script()