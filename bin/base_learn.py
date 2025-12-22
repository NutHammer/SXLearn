# 基础学习模块 - 整合重复代码

import time
from selenium.webdriver.common.by import By

# 自定义异常,用于跳出循环
class SkipToNextCourse(Exception):
    pass

class BaseLearn:
    def __init__(self, driver, max_attempts=50):
        self.driver = driver
        self.max_attempts = max_attempts
        self.driver.implicitly_wait(5)  # 设置隐式等待
    
    def new_window(self):
        """切换到新标签页"""
        current_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                break
    
    def close_windows(self):
        """关闭所有非活动标签页"""
        current_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                self.driver.close()
        self.driver.switch_to.window(current_window)  # 切换回活动标签页
    
    def switch_to_latest_window(self):
        """切换到最新标签页"""
        if self.driver.window_handles:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(3)
    
    def click_learning_classroom(self):
        """点击学习课堂按钮"""
        try:
            self.driver.find_elements(By.CLASS_NAME, "item")[2].click()
            time.sleep(3)
            return True
        except:
            print("未找到课程。请检查是否已打开学习网站并登录。")
            return False
    
    def click_enter_learning(self, button_index):
        """点击进入学习按钮"""
        try:
            btn_elements = self.driver.find_elements(By.CLASS_NAME, "btn")
            btn_elements[button_index].click()
            time.sleep(3)
            return True
        except:
            print("无可学专题")
            return False
    
    def click_start_learning(self):
        """点击开始学习/继续学习按钮"""
        try:
            btn_elements = self.driver.find_elements(By.CLASS_NAME, "btn")
            btn_elements[0].click()
            time.sleep(3)
            return True
        except:
            print("已学完")
            return False
    
    def play_videos(self):
        """播放视频列表"""
        scrollbar_views = self.driver.find_elements(By.CLASS_NAME, "el-scrollbar__view")
        self.driver.find_elements(By.CLASS_NAME, "item2")[0].click()  # 点击视频，使其开始播放
        
        # 逐个播放滚动列表中的每个视频
        for view in scrollbar_views:
            child_elements = view.find_elements(By.XPATH, "./*")
            if child_elements:
                child_elements[0].click()
                time.sleep(3)
                
                # 循环检测当前视频是否播完
                for i, child in enumerate(child_elements):
                    print("\n开始播放：", child.text)               
                    time.sleep(3)
                    error_count = 0  # 重置错误计数器
                    str0 = "200"  # 错误指标
                    
                    while True:
                        try:
                            vvstr_elements = self.driver.find_elements(By.CLASS_NAME, "vvstr")  # 获取播放进度
                            if vvstr_elements:
                                str1 = vvstr_elements[0].text[-4:]
                                if str0 != str1:
                                    error_count = 0
                                    str0 = str1
                                else:
                                    error_count += 1  # 播放进度未改变时增加错误计数
                                print(".", end="", flush=True)
                                
                                # 检查播放进度是否达到100%
                                if str1 == "100%":
                                    if i + 1 < len(child_elements):
                                        child_elements[i + 1].click()
                                        break
                                    else:
                                        print("\n本课程播放完成，准备播放下一课程")
                                        break
                            
                            # 异常次数过多时退出循环
                            if error_count >= 15:
                                print("\n检测到异常状态，尝试恢复学习流程")
                                self._recover_from_error()
                                raise SkipToNextCourse()
                            
                            time.sleep(10)
                            
                        except SkipToNextCourse as e:
                            raise
                        except Exception as e:
                            print(f"发生错误: {e}")
                            break
    
    def _recover_from_error(self):
        """从错误状态恢复"""
        current_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles
        for window in all_windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                self.driver.close()
        self.driver.switch_to.window(current_window)
        self.driver.refresh()
        time.sleep(5)
    
    def run_learning_cycle(self, button_index):
        """执行学习循环"""
        for attempt in range(self.max_attempts):
            try:
                print(f"第{attempt+1}课学习")
                
                # 点击学习课堂
                if not self.click_learning_classroom():
                    break
                
                # 点击进入学习按钮
                if not self.click_enter_learning(button_index):
                    break
                
                # 点击开始学习按钮
                if not self.click_start_learning():
                    break
                
                # 切换到新标签页并播放视频
                self.new_window()
                self.play_videos()
                
            except SkipToNextCourse:
                continue
            finally:
                self.close_windows()