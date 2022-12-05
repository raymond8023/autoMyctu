# 引用库
#import json
import argparse
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

WAIT_TIME=5

def play_video(driver):
    interval = 10
    isDone = False
    print("start play video...")
    try:
        video = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[1]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/video')
        print(driver.execute_script("return arguments[0].currentSrc;", video))
        ActionChains(driver).click(video).perform()  # 使用鼠标事件
        driver.execute_script("return arguments[0].play()", video)
    except:
        pass

    while isDone == False:
        time.sleep(interval)
        try:
            video = driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div[1]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/video')
            isDone = driver.execute_script("return arguments[0].ended;", video)
            print("播放中..." if isDone==False else "已结束！")
        except:
            pass
        # 弹窗处理：不处理
    print("this video finish")


if __name__ == '__main__':
    # 输入课程url
    parser = argparse.ArgumentParser(description='autoMyctu')
    parser.add_argument('--url', type=str, help='url')
    args = parser.parse_args()
    url = args.url
    # url = "https://kc.zhixueyun.com/#/study/subject/detail/3c1838e6-3455-4089-b502-15aca3730fc4"
    # url = "https://kc.zhixueyun.com/#/study/course/detail/10&b762264b-eda3-455d-83e2-3720874fa9ba/6/1"
    if url==None:
        url=input("please input the course url:")
    #初始化
    option = ChromeOptions()
    option.add_argument('-mute-audio')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--ignore-ssl-error')
    option.add_argument('--disable-extensions')
    option.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])
    option.add_argument('---ignore-certificate-errors-spki-list')
    option.add_argument('log-level=2')
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    driver.get(url)

    # 自动跳转到登陆页面，需要扫码登陆，登陆后进入课程页面
    print("open the page,wait for login")
    time.sleep(WAIT_TIME*2)   #跳转等待时间
    WebDriverWait(driver, 300).until(EC.url_to_be(url)) #等待登陆的时间，直到登陆完自动跳转回来
    time.sleep(WAIT_TIME*2)
    try:
        video = driver.find_element(By.XPATH,
                                '/html/body/div[1]/div[1]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/video')
        type=1  #1表示地址直接可以播放
        print("type:",type)
    except:
        type=2  #2表示需要进入每一个具体页面播放
        print("type:", type)
    if type==1:
        play_video(driver)

    elif type==2:
        original_window = driver.current_window_handle
        # 循环查询需要学的课程：开始学习 or 继续学习
        taskList = driver.find_elements(By.XPATH, '//*[@class="item current-hover"]')
        stateList = driver.find_elements(By.XPATH, '//*[@class="small inline-block"]')
        print(len(taskList),"course found.",len(stateList))
        for i in range(len(taskList)):
            print(i+1,stateList[i].text)
            if stateList[i].text == "开始学习" or stateList[i].text == "继续学习":
                #手动组装course_url
                course_url = "https://kc.zhixueyun.com/#/study/course/detail/" + "10&" + taskList[i].get_attribute('data-resource-id') + "/6/1"
                print("find the course:",course_url)
                driver.switch_to.new_window()
                time.sleep(WAIT_TIME)
                # print(driver.window_handles)
                driver.get(course_url)
                time.sleep(WAIT_TIME*2)
                #study video html5
                try:
                    video = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/video')
                    play_video(driver)
                except:
                    print("该课程不是视频，需要手动学习！")
                # print(driver.window_handles)
                time.sleep(1)
                driver.close()
                time.sleep(WAIT_TIME/2)
                driver.switch_to.window(original_window)
                time.sleep(WAIT_TIME)
    print("study complete!")


