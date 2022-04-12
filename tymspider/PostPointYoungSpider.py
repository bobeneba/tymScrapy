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


class PostPointYoungSpider(scrapy.Spider):

    name = "PostPointYoung"



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
            "pointyoung": "https://quannan.netalent.cn:8086/quannanv3/api/pointYouth/save",
            "getBuildingIdByCardId" :"http://localhost:9001/api/getBuildingIdByCardId",
            "getBuildingIdByName" : "http://localhost:9001/api/getBuildingIdByName"

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


        url = self.base_url['getBuildingIdByCardId']
        self.headers ={}
        self.headers["Content-Type"]="application/json;charset=UTF-8"
        self.headers["Accept"]="application/json"
        self.headers["zeus-token"]=cookie_items[0]["value"]

        for (region_no,idcard,name_person,youth_type,familySituation,guardianRelative,helpContact,helpMethod,helpName) in self.data:
            api_data = {}
            api_data['idcard'] = idcard
            item_no = {}
            item_no["regionNo"] =str(region_no)
            item_no["name"] = str(name_person)
            item_no["youthType"] = str(youth_type)
            item_no["familySituation"] =str(familySituation)
            item_no["guardianRelative"] = str(guardianRelative)
            item_no["helpContact"] = str(helpContact)
            item_no["helpMethod"] = str(helpMethod)
            item_no["helpName"] = str(helpName)


            self.count = self.count + 1

            yield Request(url, method="POST",
                          headers=self.headers, body=json.dumps(api_data,ensure_ascii=False),
                          cookies=self.cookiedict,meta=item_no, callback=self.parseBuildId,dont_filter=True)

            # yield JsonRequest(url,data=api_data, , callback=self.parse_json)

    def parseBuildId(self,response):

        res_data = json.loads(response.body.decode('utf-8'))
        #print(res_data)
        url = self.base_url["getBuildingIdByName"]
        item_no = response.meta
        item_no["personId"] = res_data["id"]
        api_data = {}
        api_data["name"] = item_no["helpName"]
    #    api_data["regionNo"] = item_no["regionNo"]

        self.code = self.code + 1;

        if "code" in res_data:

            print("[info]:::::::::::::buildId fails 1 :::::::::::::::::::::::::::::::: ")
        else:

            yield Request(url, method="POST",
                          headers=self.headers, body=json.dumps(api_data),
                          cookies=self.cookiedict, meta=item_no, callback=self.parseBuildName,dont_filter=True)

        # yield Request(url, method="POST",
        #               headers=self.headers, body=json.dumps(api_data),
        #               cookies=self.cookiedict, callback=self.parse_json)

    def parseBuildName(self,response):
        res_data = json.loads(response.body.decode('utf-8'))
        print(res_data)
        url = self.base_url["pointyoung"]

        self.code = self.code + 1;

        if "code" in res_data:

            print("[info]:::::::::::::buildId fails  2  :::::::::::::::::::::::::::::::: ")
        else:
            item_no = response.meta
            guardianId = res_data["id"]

            api_data = {}
            api_data["personId"] = item_no["personId"]
            api_data["isCrime"] = "false"
            if("闲散青少年" in str(item_no["youthType"])):
                api_data["youthType"] = str("100208")
            if("不良行为" in str(item_no["youthType"])):
                api_data["youthType"] = str("100209")
            if ("刑满" in str(item_no["youthType"])):
                api_data["youthType"] = str("100209")
            if ("服刑" in str(item_no["youthType"])):
                api_data["youthType"] = str("100211")
            if ("农村" in str(item_no["youthType"])):
                api_data["youthType"] = str("100212")
            if ("其他" in str(item_no["youthType"])):
                api_data["youthType"] = str("100213")
            api_data["guardianId"] = guardianId
            api_data["familySituation"] = item_no["familySituation"]
            api_data["guardianRelative"] = item_no["guardianRelative"]
            api_data["helpContact"] = item_no["helpContact"]
            api_data["helpMethod"] = item_no["helpMethod"]
            api_data["helpName"] = item_no["helpName"]
            #print(json.dumps(api_data))

            yield Request(url, method="POST",
                          headers=self.headers, body=json.dumps(api_data),
                          cookies=self.cookiedict, callback=self.parse_json, dont_filter=True)



    def parse_json(self, response):
        res_data = json.loads(response.body.decode('utf-8'))

        print(res_data)
        if (res_data["code"] == "200"):
            self.success = self.success + 1
            print("success: "+str(self.success)+"fails:"+str(self.fails)+" code "+str(self.code)+"count: "+str(self.count))


        # print("[info]:::::::::::::insert sucess:::::::::::::::::::::::::::::::: [count]: "+str(self.success)+" cidcard: "+str(idcard))
        else:

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
        sql_select = "select region_no,idcard,name_person,youth_type,familySituation,guardianRelative,helpContact,helpMethod,helpName from pointYouth  "
        result = self.cursor.execute(sql_select).fetchall()
        print(1)
        return result
