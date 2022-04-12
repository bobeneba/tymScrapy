# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from itemadapter import ItemAdapter


class TymspiderPipeline:
    def open_spider(self,spider):
        self.db_name= "quannan1"
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()


    def close_spider(self,spider):
        pass
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.inser_data(item,spider)
        return item

    def inser_data(self,item,spider):
        if(spider.name=="yunlong"):
            # values = {
            #     item['region_no'],
            #     item['name'],
            #     item['person_type'],
            #     item['nowland'],
            #     item['registered_place'],
            #     item['idcard'],
            #     item['sex'],
            #     item['nation'],
            #     item['birthday'],
            #     item['contact']
            # }

            insert_sql = 'insert into base_person1 (region_no,name,person_type,nowland,registered_place,idcard,sex,nation,birthday,contact) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['name'], item['person_type'], item['nowland'], item['registered_place'],
                item['idcard'], item['sex'], item['nation'], item['birthday'], item['contact'])
            result = self.cursor.execute(insert_sql)
        elif spider.name == "populations":

            print("hehehe")

            pass
        else:
            pass
        print("[Info]:::::Insert data to sqlite3:::::::[region_no] ", item['region_no'])
        #
        # print(result)



