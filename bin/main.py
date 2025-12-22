#  程序入口、初始化、交互界面
from base_learn import BaseLearn
import chromedriver

#  选择执行脚本函数
def run_selected_script():
    print("陕西干部网络学院刷课工具")
    web_address = "https://www.sqgj.gov.cn/index"
    driver = chromedriver.auto_chrome(web_address)
    while True:
        # 显示菜单选项
        print("="*25)
        print("输入 0 完成网络自学")
        print("输入 整数n 完成第n个专题学习") 
        print("输入 A 学习全部课程")
        print("输入 Q 退出程序")
        
        # 选择功能
        choice = input("请输入：")
        
        if choice.lower() == 'q':
            print("程序退出")
            break
        elif choice.lower() == 'a':
            print("开始学习所有课程...")
            for i in range(10):
                try:
                    print(f"\n正在学习专题 {i}...")
                    learner = BaseLearn(driver)
                    learner.run_learning_cycle(button_index=i)
                except Exception as e:
                    print(f"\n专题 {i} 已学完或发生错误")
                    print("继续执行下一个专题...")
        else:
            try:
                choice = int(choice)
                if 0 <= choice <= 9:
                    learner = BaseLearn(driver)
                    learner.run_learning_cycle(button_index=choice)
            except ValueError:
                print("请输入有效的整数（0-9）或A（执行所有选项）")

if __name__ == "__main__":
    run_selected_script()