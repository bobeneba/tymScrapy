import json
import os
import re
import sqlite3
from asyncio import sleep

import scrapy
from scrapy import Request



from ..items import TymspiderItem

class YunlongSpider(scrapy.Spider):

    name = "yunlong"

    def start_requests(self):
        self.base_url = {
           # "cirs":"http://172.10.128.130:10004/cirs/getListData.jhtml?",
           # "100705":"http://172.10.128.130:10004/rspermanent/getListData.jhtml?",
            "100706":"http://172.10.128.130:10004/flow/getListData.jhtml?",
           # "100707":"http://172.10.128.130:10004/leftBehind/getListData.jhtml?"
        }

        cookieStr ="UAM_TOKEN_FLAG=0; resourcekey=V6q72kt3G3uF1cB8pbKvg8rIo4k9n6FlCwKWlaBnQ7oClK+VAe91dZYokmCMJaPJ/ZlGwmK0TB9GMWPhmPMCZA==; UAM_SESSIONID=22F11330FD72540FEFFA2F12A0F65DB8; resource=2ZwSxu0ntvGhJ04X1RCqcYpEFmGEtu34BvPASwVcPWGB+RNuwU6Cjv/HrulmnpCl; JSESSIONID=52E6D31F448C077721F6E18F417818E6"
        self.cookiedict = dict(line.split("=", 1) for line in cookieStr.split("; "))

        print(self.cookiedict)
        self.init_sqlite3()
        codeList =self.get_url()
        for key,value_url in self.base_url.items():

            for code in codeList:
                no = code[1]
                item_no = {}
                item_no["no"] = str(no);
                item_no["url"] = str(value_url)
                item_no["crawl_type"] = str(key)
                url = value_url + "orgCode=" + str(code[0]).strip() + "&dataStatus=001&page=1&rows=20"
                # url="http://172.10.128.130:10004/cirs/getListData.jhtml?orgCode=360729203&dataStatus=001&page=3&rows=20"

                print("[Info]::::::::url orgCode createFactory :::::::::[url]::", url)

                yield Request(url, method="POST",
                              headers={'Content-Type': 'application/json;charset=UTF-8', "Accept": "application/json"},
                              cookies=self.cookiedict, meta=item_no, callback=self.parse_json)

    def parse_json(self, response):
        res_data = json.loads(response.body.decode('utf-8'))
        total=int(res_data['total'])
        url_from = response.url
        orgcode = re.findall(r"orgCode=(.+)&d",url_from)
        mate_item = response.meta
        crawl_url=mate_item['url']

        print("[Info]:::::rows total::::::: [total]::",total)

        if(int(total/1000)==0):
            url = crawl_url + "orgCode=" + str(orgcode[0]).strip() + "&dataStatus=001&"
            url = url + "page=1"+"&rows="+str(total)

            print("[Info]:::::[row<1000]::[page 1]:::ture spider page crawler URL::::::: [url]::",url)

            yield Request(url, method="POST", headers={'Content-Type': 'application/json;charset=UTF-8',
                                                       "Accept": "application/json"}, cookies=self.cookiedict,
                          callback=self.parse_item,meta=mate_item, dont_filter=True)

        else:
            for page in range((int(total / 1000)+1)):
                if ((total - (page) * 1000) >= 1000):
                    #url = url + "page=" + str(page + 1) + "&rows=1000"
                    url = crawl_url + "orgCode=" + str(orgcode[0]).strip() + "&dataStatus=001&"
                    url = url + "page=" + str(page + 1) + "&rows=1000"

                    print("[Info]:::::[row>1000]::[page number]::ture spider crawler URL::::::: [url]:",url)

                    yield Request(url, method="POST", headers={'Content-Type': 'application/json;charset=UTF-8',
                                                               "Accept": "application/json"}, cookies=self.cookiedict,
                                  callback=self.parse_item,meta=mate_item,dont_filter=True)
                else:
                    rows = total - (page) * 1000
                    url = crawl_url + "orgCode=" + str(orgcode[0]).strip() + "&dataStatus=001&"
                    url = url + "page=" + str(page + 1) + "&rows=" + str(1000)

                    print("[Info]:::::[row>1000]::[page end]::ture spider crawler URL::::::: [url]:",url)

                    yield Request(url, method="POST", headers={'Content-Type': 'application/json;charset=UTF-8',
                                                               "Accept": "application/json"}, cookies=self.cookiedict,
                                  callback=self.parse_item,meta=mate_item,dont_filter=True)

    def parse_item(self, response):
        item = TymspiderItem()
        region_no = response.meta['no']
        crawl_type = response.meta['crawl_type']
        res_data = json.loads(response.body.decode('utf-8'))
        res_rows = res_data["rows"]

        print("[Info]:::::::::::::spider parse item url::::::::::::[url]:",response.url)

        for row in res_rows:
            item["region_no"]=str(region_no)
            item["name"] = row["partyName"]
            item["person_type"] =str(crawl_type)
            if(hasattr(row,"residenceAddr")==True):
                item["nowland"] = row["residenceAddr"]
            else:
                item["nowland"] = " "
            item["registered_place"] = row["residence"]
            item["idcard"] = row["identityCard"]
            item["sex"] = row["genderCN"]
            item["nation"]= row["nationCN"]
            item["birthday"]=row["birthday"]
            item["contact"]=row["mobilePhone"]
            #print(item)
            yield item



    def open_sqlite3(self):
        self.db_name = "quannan"
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close_sqlite3(self):
        self.conn.commit()
        self.conn.close()

    def init_sqlite3(self):
        self.open_sqlite3()
        self.createtable_sqlite3()
        self.insert_sqlite3()

    def insert_sqlite3(self):

        sql_insert_flag = "select count(*) as total from per_region"
        result = self.cursor.execute(sql_insert_flag)
        total = result.fetchone()[0]
        if (int(total) == 0):
            with open("per_region.json", "r", encoding='UTF-8') as f:
                self.load_dict = json.load(f)
            for item in self.load_dict['RECORDS']:
                self.insert_data(item)
            self.close_sqlite3()

    def createtable_sqlite3(self):
        sql_create = "create table if not exists per_region (id int not null,name text,no text,parent_id text,fullname text,region_typetext,code text,cid text)"
        self.cursor.execute(sql_create)

    def insert_data(self, item):
        values = (
            int(item['id']),
            item['name'],
            item['no'],
            item['parent_id'],
            item['fullname'],
            item['region_type'],
            item['code'],
            item['cid']
        )
        sql = 'insert into per_region VALUES(?,?,?,?,?,?,?,?)'
        result = self.cursor.execute(sql, values)

        print(result)

    def get_url(self):
        sql_code='select code ,no  from per_region where length(no)=20'
        result = self.cursor.execute(sql_code).fetchall()
        return result

