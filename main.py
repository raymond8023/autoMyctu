# 引用库
#import json
import argparse
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    # 录入账号，输入验证码
    '''
    #切换标签填写手机号account并发送验证码
    try:
        iframe = driver.find_element(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(iframe)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/video').click()
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[3]/div[2]/input').send_keys(account)
        driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[2]/div[3]/div[4]/span[2]').click()
    except:
        pass
    '''
    # 开始学习studyStart
    # 学习结束studyEnd
    # 更新本次学习概况：courseCnt，studyDuration
    # HTML5播放器的相关操作
    '''
    print(video.get_attribute('title'))    # 需要验证结束时是否会有title
    print(driver.execute_script("return arguments[0].duration;", video))
    print(driver.execute_script("return arguments[0].ended;", video))
    driver.execute_script("return arguments[0].currentSrc;", video)
    driver.execute_script("return arguments[0].play()", video)
    driver.execute_script("return arguments[0].pause()", video)
    '''
    # cookie相关（没试成功）
    '''
    with open('cookies.txt', 'w') as f:
        # 将cookies保存为json格式
        f.write(json.dumps(driver.get_cookies()))
    driver.get("https://kc.zhixueyun.com/404.html")
    driver.delete_all_cookies()
    with open('cookies.txt', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        for cookie in cookies_list:
            driver.add_cookie(cookie)
    driver.refresh()    
    '''


    # 输入课程url
    parser = argparse.ArgumentParser(description='autoMyctu')
    parser.add_argument('--url', type=str, help='url')
    args = parser.parse_args()
    url = args.url
    if url==None:
        url=input("please input the course url:")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    print("open the page,wait for login")
    # 自动跳转到登陆页面，需要扫码登陆，登陆后进入课程页面
    time.sleep(30)    #等待登陆的时间
    studyDone=0 #标志是否完成所有课程的学习
    original_window = driver.current_window_handle
    print(original_window)
    # 循环查询需要学的课程：开始学习 or 继续学习
    while studyDone==0:
        studyDone=1
        taskList = driver.find_elements(By.XPATH, '//*[@class="item current-hover"]')
        print(len(taskList),"course found.")
        for task in taskList:
            state = task.find_element(By.XPATH, '//*[@class="small inline-block"]')
            print(state.text)
            if state.text == "开始学习" or state.text == "继续学习":
                studyDone=0
                #task.click()   #点击进去获取不到新窗口的handle
                #手动组装course_url
                course_url = "https://kc.zhixueyun.com/#/study/course/detail/" + "10&" + task.get_attribute('data-resource-id') + "/6/1"
                print("find the course:",course_url)
                driver.switch_to.new_window()
                time.sleep(1)
                print(driver.window_handles)
                driver.get(course_url)
                time.sleep(5)
                #study video html5
                video = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/video')
                print(driver.execute_script("return arguments[0].currentSrc;", video))
                try:
                    ActionChains(driver).click(video).perform() #使用鼠标事件
                    driver.execute_script("return arguments[0].play()", video)
                except:
                    pass
                while driver.execute_script("return arguments[0].ended;", video)==False:
                    time.sleep(60)
                    #弹窗处理：不处理
                print(driver.window_handles)
                driver.close()
                driver.switch_to.window(original_window)

    print("study complete!")


