from selenium import webdriver
import os
import urllib.request
import time

def crawl(keywords, number):
    path = "https://www.google.com/search?q=" + keywords + "&newwindow=1&rlz=1C1CAFC_enKR908KR909&sxsrf=ALeKk01k_BlEDFe_0Pv51JmAEBgk0mT4SA:1600412339309&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj07OnHkPLrAhUiyosBHZvSBIUQ_AUoAXoECA4QAw&biw=1536&bih=754"
    driver = webdriver.Chrome('./chromedriver')
    # 다음 웹페이지가 넘어 올때까지 기다리기
    driver.implicitly_wait(3)

    driver.get(path)
    # 전체화면으로 바꾸기
    driver.maximize_window()
    time.sleep(1)
    
    # 폴더생성
    os.makedirs(keywords, exist_ok=True)
    
    counter = 0
    flag = False
    while True:
        # 페이지 끝까지 스크롤을 내림
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        for x in driver.find_elements_by_class_name('rg_i.Q4LuWd'):
            # 이미지 url
            img = x.get_attribute("data-src")
            if img is None:
                img = x.get_attribute("src")
            print(img)

            # 구글 이미지를 읽고 저장한다.
            try:
                raw_img = urllib.request.urlopen(img).read()
                File = open(os.path.join(keywords, keywords + "_" + str(counter) + ".jpg"), "wb")
                File.write(raw_img)
                File.close()
                counter = counter + 1
            except:
                print('error')
            
            if counter == number:
                flag = True
                break
        if flag:
            break 

    driver.close()


crawl("test", 500)
