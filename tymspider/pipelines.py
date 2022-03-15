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
            #result = self.cursor.execute(insert_sql)


        elif spider.name == "populations":

            insert_sql = 'insert into pointYouth (region_no,crawl_type,idcard,name_person,nowland,youth_type,person_id,crimeSituation,familySituation,guardianId,guardianRelative,helpContact,helpMethod,helpName,helpSituation,isCrime) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['idcard'], item['name_person'], item['nowland'],
                item['youth_type'], item['person_id'], item['crimeSituation'], item['familySituation'],
                item['guardianId'], item['guardianRelative'], item['helpContact'], item['helpMethod'], item['helpName'],
                item['helpSituation'],
                item['isCrime'])
            print(insert_sql)
            #result = self.cursor.execute(insert_sql)
            #print("hehehe")

        elif spider.name == "ReleaseCriminal":

            insert_sql = 'insert into releaseCriminal (region_no,crawl_type,idcard,name_person,accusationType,sentence,releaseDate,servingPlace,dangerEstimateType,connectDate,connectCondition,settleDate,settleCondition,unsettleReason,educate,isRecidivist,isRepeat) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['region_no'], item['crawl_type'], item['idcard'], item['name_person'], item['accusationType'],
                item['sentence'], item['releaseDate'], item['servingPlace'], item['dangerEstimateType'],
                item['connectDate'], item['connectCondition'], item['settleDate'], item['settleCondition'], item['unsettleReason'],
                item['educate'],
                item['isRecidivist'],item["isRepeat"])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "Basebuilding":

            insert_sql = 'insert into base_building (region_no,crawl_type,name,floor,code,address) values ("{}", "{}", "{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['name'], item['floor'], item['code'],
                item['address'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "Community":

            insert_sql = 'insert into community (region_no,crawl_type,idcard,name,rectificationType,caseType,specificAccusation,receiveWay,rectificationStart,rectificationEnd) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['idcard'], item['name'], item['rectificationType'],
                item['caseType'],item['specificAccusation'], item['receiveWay'], item['rectificationStart'],
                item['rectificationEnd'])
            print(insert_sql)
            print("test")
           # result = self.cursor.execute(insert_sql)

        elif spider.name == "CauseTrouble":

            insert_sql = 'insert into CauseTrouble (region_no,crawl_type,idcard,name,guardianName,guardianContact,diagnosisType,dangerEstimateLevel,cure) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['idcard'], item['name'], item['guardianName'],
                item['guardianContact'], item['diagnosisType'], item['dangerEstimateLevel'], item['cure'])
            print(insert_sql)
            print("test")
           # result = self.cursor.execute(insert_sql)

        elif spider.name == "Drug":

            insert_sql = 'insert into Drug (region_no,crawl_type,idcard,name) values ("{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['idcard'], item['name'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "Keyperson":

            insert_sql = 'insert into keyperson (region_no,crawl_type,idcard,name,interviewReason,officialsName,chargeName,visitNum) values ("{}", "{}", "{}", "{}","{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['idcard'], item['name'],item['interviewReason'], item['officialsName'], item['chargeName'], item['visitNum'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "Enterprise":

            insert_sql = 'insert into enterprise (region_no,crawl_type,type,enterpriseType,contact,name,corAddr,respoName) values ("{}", "{}", "{}", "{}","{}", "{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['type'], item['enterpriseType'],item['contact'], item['name'], item['corAddr'], item['respoName'])
            print(insert_sql)
            print("test")
           # result = self.cursor.execute(insert_sql)

        elif spider.name == "Organization":

            insert_sql = 'insert into organization (region_no,crawl_type,type,organizationType,name,aim) values ("{}", "{}", "{}", "{}","{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['type'], item['organizationType'], item['name'],
                item['aim'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "Institution":

            insert_sql = 'insert into institution (region_no,crawl_type,institutionName,institutionType,institutionLevel) values ("{}", "{}", "{}", "{}","{}")'.format(
                item['region_no'], item['crawl_type'], item['institutionName'], item['institutionType'], item['institutionLevel'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "InstitutionTeam":

            insert_sql = 'insert into institutionTeam (region_no,crawl_type,institutionId,phone,administrationLevel,name,idCard,born,sexStr) values ("{}", "{}", "{}", "{}","{}","{}", "{}", "{}","{}")'.format(
                item['region_no'], item['crawl_type'], item['institutionId'], item['phone'],
                item['administrationLevel'], item['name'], item['idCard'], item['born'],
                item['sexStr'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)


        elif spider.name == "DefenseOrg":

            insert_sql = 'insert into defenseOrg (region_no,crawl_type,organizationName,organizationType,mainFunc,manager,teamTypeStr) values ("{}", "{}", "{}", "{}","{}","{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['organizationName'], item['organizationType'],
                item['mainFunc'], item['manager'], item['teamTypeStr'])
            print(insert_sql)
            print("test")
           # result = self.cursor.execute(insert_sql)

        elif spider.name == "DefenseTeam":

            insert_sql = 'insert into defenseTeam (region_no,crawl_type,institutionId,phone,administrationLevel,name,idCard,born,sexStr) values ("{}", "{}", "{}", "{}","{}","{}", "{}", "{}","{}")'.format(
                item['region_no'], item['crawl_type'], item['institutionId'], item['phone'],
                item['administrationLevel'], item['name'], item['idCard'], item['born'],
                item['sexStr'])
            print(insert_sql)
            print("test")
            #result = self.cursor.execute(insert_sql)

        elif spider.name == "DefenseOrg":

            insert_sql = 'insert into defenseOrg (region_no,crawl_type,organizationName,organizationType,mainFunc,manager,teamTypeStr) values ("{}", "{}", "{}", "{}","{}","{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['organizationName'], item['organizationType'],
                item['mainFunc'], item['manager'], item['teamTypeStr'])
            print(insert_sql)
            print("test")
           # result = self.cursor.execute(insert_sql)

        elif spider.name == "Cent":

            insert_sql = 'insert into cent (region_no,crawl_type,idCard,centerName,centerContact,chargeName,address,centerLevel) values ("{}", "{}", "{}", "{}","{}","{}", "{}", "{}")'.format(
                item['region_no'], item['crawl_type'], item['idCard'], item['centerName'],
                item['centerContact'], item['chargeName'], item['address'], item['centerLevel'])
            print(insert_sql)
            print("test")
            result = self.cursor.execute(insert_sql)

        else:
            pass
        print("[Info]:::::Insert data to sqlite3:::::::[region_no] ", item['region_no'])
        #
        # print(result)



