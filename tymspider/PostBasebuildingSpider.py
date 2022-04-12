import json
import os
import re
import sqlite3
from asyncio import sleep

from scrapy.http import JsonRequest


import scrapy
from scrapy import Request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import request


class PostBasePersonSpider(scrapy.Spider):

    name = "Postbuilding"



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
            "baseperson": "https://quannan.netalent.cn:8086/quannanv3/api/building/save"
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


        url = self.base_url['baseperson']
        self.headers ={}
        self.headers["Content-Type"]="application/json;charset=UTF-8"
        self.headers["Accept"]="application/json"
        self.headers["zeus-token"]=cookie_items[0]["value"]

        for (region_no,name,floor,address) in self.data:
            api_data = {}
            api_data['regionNo'] = region_no
            api_data['name'] = name
            api_data['buildCharacter'] = '101175'
            api_data['buildUseType'] ='101130'
            api_data['buildType'] ='101136'
            api_data['floor'] = floor
            api_data['address'] = address
           # api_data['isPropertyRight'] ='false'

            # api_data['personType'] = person_type
            # api_data['nowland'] = nowland
            # api_data['registeredPlace'] = registered_place
            # api_data['idcard'] = idcard
            # if (sex == "女性"):
            #     api_data['sex'] = "100498"
            # elif (sex == "男性"):
            #     api_data['sex'] = "100497"
            # else:
            #     api_data['sex'] = "100499"
            # if(nation=="汉族"):
            #     api_data['nation'] = "100556"
            # else:
            #     api_data['nation'] = "100612"
            # api_data['birthday'] = birthday
            # api_data['contact'] = contact
            #
            # api_data['registeredPlaceNum'] = "100612"
            # temp=json.dumps(api_data,ensure_ascii=False)
            #print(json.dumps(api_data,ensure_ascii=False))
            # metadata={};
            # metadata['idcard']=idcard

            yield Request(url, method="POST",
                              headers=self.headers,body=json.dumps(api_data),
                              cookies=self.cookiedict, callback=self.parse_json)
            # yield JsonRequest(url,data=api_data, , callback=self.parse_json)
    def parse_json(self, response):
        res_data = json.loads(response.body.decode('utf-8'))

        # idcard = response.meta['idcard']
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
        sql_select = "select region_no, name,max(floor) as floor,address from base_building group by name,region_no"
        result = self.cursor.execute(sql_select).fetchall()
        print(1)
        return result
