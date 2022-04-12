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


class PostCauseTroubleSpider(scrapy.Spider):

    name = "PostCauseTrouble"



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
            "PostCauseTrouble": "https://quannan.netalent.cn:8086/quannanv3/api/causeTrouble/save",
            "basepersonId": "http://localhost:9001/api/getBuildingIdByCardId"
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

        for (idcard ,guardianName ,guardianContact ,diagnosisType ,dangerEstimateLevel ,cure  ) in self.data:
            api_data = {}
            api_data['idcard'] = idcard
            item_no = {}
            item_no["guardianName"]=str(guardianName)
            item_no["guardianContact"]=str(guardianContact)

            if("精神分裂症" in str(diagnosisType)):
                item_no["rectificationType"] = str(100397)
            if("其他" in str(diagnosisType)):
                item_no["diagnosisType"] = str(100405)
            if ("双相" in str(diagnosisType)):
                item_no["rectificationType"] = str(100400)
            if ("癫痫" in str(diagnosisType)):
                item_no["diagnosisType"] = str(100401)
            if ("精神活性" in str(diagnosisType)):
                item_no["diagnosisType"] = str(100404)
            else:
                item_no["diagnosisType"] = str(100405)

            if ("0" in str(dangerEstimateLevel)):
                item_no["dangerEstimateLevel"] = str(100406)
            if ("1" in str(dangerEstimateLevel)):
                item_no["dangerEstimateLevel"] = str(100407)
            if ("2" in str(dangerEstimateLevel)):
                item_no["dangerEstimateLevel"] = str(100408)
            if ("3" in str(dangerEstimateLevel)):
                item_no["dangerEstimateLevel"] = str(100409)
            if ("4" in str(dangerEstimateLevel)):
                item_no["dangerEstimateLevel"] = str(100410)
            else:
                item_no["dangerEstimateLevel"] = str(100406)

            item_no["cure"] = str(100414)

            self.count = self.count + 1

            yield Request(url, method="POST",
                          headers=self.headers, body=json.dumps(api_data,ensure_ascii=False),
                          cookies=self.cookiedict,meta=item_no, callback=self.parseBuildId,dont_filter=True)

            # yield JsonRequest(url,data=api_data, , callback=self.parse_json)

    def parseBuildId(self,response):

        res_data = json.loads(response.body.decode('utf-8'))
        #print(res_data)
        url = self.base_url["PostCauseTrouble"]
        mate_item = response.meta
        api_data = {}
        api_data['personId'] = str(res_data["id"])
        api_data["guardianName"]=mate_item["guardianName"]
        api_data["guardianContact"]=mate_item["guardianContact"]
        api_data["dangerEstimateLevel"]=mate_item["dangerEstimateLevel"]
        api_data["cure"]=mate_item["cure"]



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
        sql_select = "select idcard ,guardianName ,guardianContact ,diagnosisType ,dangerEstimateLevel ,cure from CauseTrouble "
        result = self.cursor.execute(sql_select).fetchall()
        print(1)
        return result
