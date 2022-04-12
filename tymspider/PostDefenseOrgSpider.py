import json
import os
import re
import sqlite3





import scrapy
from scrapy import Request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import request


class PostDefenseOrgSpider(scrapy.Spider):

    name = "DefenseOrg"



    def start_requests(self):
        window = webdriver.Chrome()
        window.maximize_window()
        window.get("https://quannan.netalent.cn:8086/quannan_v3.web/login.html")

        # 输入账号
        input_account = window.find_element(By.XPATH, '//form/div[2]/input')
        input_account.send_keys('admindt')
        # 输入密码
        input_password = window.find_element(By.XPATH, '//form/div[4]/input')
        input_password.send_keys('admindt123456')

        # 获取验证码图片

        # img_ele = window.find_element(By.XPATH, '//*[@id="send"]/img')
        # src = img_ele.get_attribute('src')
        #
        # request.urlretrieve(src, './img_1.png')
        # print('图片已保存')

        time.sleep(1)
        login_button = window.find_element(By.XPATH, '//form/div[6]/button')
        login_button.click()
        time.sleep(2)
        cookie_items = window.get_cookies()
        print(cookie_items)
        window.close()


        self.base_url = {
            "DefenseOrg": "https://quannan.netalent.cn:8086/quannanv3/api/defenseOrg/save"
        }
        self.cookiedict = {}
        self.cookiedict["zeus-token"] = cookie_items[0]["value"]

        # for cookie in cookie_items:
        #     self.cookiedict[cookie["name"]]=cookie["value"]
        # print(self.cookiedict)

        # self.init_sqlite3()
        self.data = self.getdata()
        self.close_sqlite3()
        self.success=0
        self.fails=0


        url = self.base_url['DefenseOrg']
        self.headers ={}
        self.headers["Content-Type"]="application/json;charset=UTF-8"
        self.headers["Accept"]="application/json"
        self.headers["zeus-token"]=cookie_items[0]["value"]

        for (region_no,organizationName,organizationType,mainFunc,teamTypeStr) in self.data:
            api_data = {}
            api_data['regionNo'] = str(region_no)
            api_data['organizationName'] = str(organizationName)
            api_data['department']=str(teamTypeStr)
            api_data['mainFunction'] = str(mainFunc)
            api_data['organizationType'] = str(101153)

            if("中央" in str(organizationType)):
                api_data['organizationLevel']=str(100260)
            elif("地" in str(organizationType)):
                api_data['organizationLevel'] = str(100262)
            elif("县" in str(organizationType)):
                api_data['organizationLevel'] = str(100263)
            elif ("乡" in str(organizationType)):
                api_data['organizationLevel'] = str(100264)
            elif ("村" in str(organizationType)):
                api_data['organizationLevel'] = str(100265)
            else:
                pass


            print(json.dumps(api_data,ensure_ascii=False))
            yield Request(url, method="POST",
                              headers=self.headers,body=json.dumps(api_data),
                              cookies=self.cookiedict, callback=self.parse_json,dont_filter=True)

    def parse_json(self, response):
        res_data = json.loads(response.body.decode('utf-8'))

        # idcard = response.meta['idcard']
        print(res_data)
        if(res_data["code"]=="200"):
            self.success=self.success+1
           # print("[info]:::::::::::::insert sucess:::::::::::::::::::::::::::::::: [count]: "+str(self.success)+" cidcard: "+str(idcard))
        else:
            print(res_data)
            self.fails=self.fails+1
            print("[info]:::::::::::::insert fails::::::::::::::::::::::::::::::::  [count]:  "+str(self.fails)+" success "+str(self.success))

        pass





    def open_sqlite3(self):
        self.db_name = "quannan1"
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close_sqlite3(self):
        self.conn.commit()
        self.conn.close()

    def getdata(self):
        self.open_sqlite3()
        sql_select = "select region_no,organizationName,organizationType,mainFunc,teamTypeStr from defenseOrg"
        result = self.cursor.execute(sql_select).fetchall()
        print(1)
        return result
