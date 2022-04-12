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


class PostCommunitySpider(scrapy.Spider):

    name = "Community"



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
            "Community": "https://quannan.netalent.cn:8086/quannanv3/api/community/save",
            "basepersonId" : "http://localhost:9001/api/getBuildingIdByCardId"
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
        self.code=0
        self.count=0


        url = self.base_url['basepersonId']
        self.headers ={}
        self.headers["Content-Type"]="application/json;charset=UTF-8"
        self.headers["Accept"]="application/json"
        self.headers["zeus-token"]=cookie_items[0]["value"]

        for (idcard,rectificationType,caseType,specificAccusation,receiveWay,rectificationStart,rectificationEnd ) in self.data:
            api_data = {}
            api_data['idcard'] = idcard
            item_no = {}
            if("2" in str(rectificationType)):
                item_no["rectificationType"] = str(100433)
            if("4" in str(rectificationType)):
                item_no["rectificationType"] = str(100435)
            else:
                item_no["rectificationType"] = str(100433)


            item_no["caseType"] = str(100441)
            item_no["specificAccusation"] = str(specificAccusation)
            item_no["receiveWay"] = str(100445)
            item_no["rectificationStart"] = str(rectificationStart)
            item_no["rectificationEnd"] = str(rectificationEnd)


            self.count = self.count + 1

            yield Request(url, method="POST",
                          headers=self.headers, body=json.dumps(api_data,ensure_ascii=False),
                          cookies=self.cookiedict,meta=item_no, callback=self.parseBuildId,dont_filter=True)

            # yield JsonRequest(url,data=api_data, , callback=self.parse_json)

    def parseBuildId(self,response):

        res_data = json.loads(response.body.decode('utf-8'))
        #print(res_data)
        url = self.base_url["Community"]
        mate_item = response.meta
        api_data = {}
        api_data['personId'] = str(res_data["id"])
        api_data["rectificationType"]=mate_item["rectificationType"]
        api_data["caseType"]=mate_item["caseType"]
        api_data["specificAccusation"]=mate_item["specificAccusation"]
        api_data["receiveWay"]=mate_item["receiveWay"]
        api_data["rectificationStart"] = mate_item["rectificationStart"]
        api_data["rectificationEnd"] = mate_item["rectificationEnd"]


        print(json.dumps(api_data,ensure_ascii=False))
        self.code = self.code + 1;

        if "code" in res_data:



            print("[info]:::::::::::::buildId fails:::::::::::::::::::::::::::::::: ")
        else:

            yield Request(url, method="POST",
                          headers=self.headers, body=json.dumps(api_data),
                          cookies=self.cookiedict,  callback=self.parse_json,dont_filter=True)

        # yield Request(url, method="POST",
        #               headers=self.headers, body=json.dumps(api_data),
        #               cookies=self.cookiedict, callback=self.parse_json)


    def parse_json(self, response):
        res_data = json.loads(response.body.decode('utf-8'))

        #print(res_data)
        if (res_data["code"] == "200"):
            self.success = self.success + 1
            print("success: "+str(self.success)+"fails:"+str(self.fails)+" code "+str(self.code)+"count: "+str(self.count))


        # print("[info]:::::::::::::insert sucess:::::::::::::::::::::::::::::::: [count]: "+str(self.success)+" cidcard: "+str(idcard))
        else:
            self.fails = self.fails + 1
            print("success: " + str(self.success))
            #print(res_data)
            print("[info]:::::::::::::insert fails::::::::::::::::::::::::::::::::  [count]:  " )


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
        sql_select = "select idcard,rectificationType,caseType,specificAccusation,receiveWay,rectificationStart,rectificationEnd from community "
        result = self.cursor.execute(sql_select).fetchall()
        print(1)
        return result
