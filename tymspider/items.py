# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TymspiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    region_no = scrapy.Field()
    name = scrapy.Field()
    person_type = scrapy.Field()
    nowland =scrapy.Field()
    registered_place=scrapy.Field()
    idcard=scrapy.Field()
    sex =scrapy.Field()
    nation =scrapy.Field()
    birthday =scrapy.Field()
    contact =scrapy.Field()

class PopulationsItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idcard = scrapy.Field()
    name_person = scrapy.Field()

    nowland = scrapy.Field()
    youth_type = scrapy.Field()
    person_id = scrapy.Field()
    crimeSituation = scrapy.Field()
    familySituation = scrapy.Field()
    guardianId = scrapy.Field()
    helpName = scrapy.Field()
    guardianRelative = scrapy.Field()
    helpContact = scrapy.Field()
    helpMethod = scrapy.Field()
    helpSituation = scrapy.Field()
    isCrime = scrapy.Field()

class ReleaseCriminalItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idcard = scrapy.Field()
    name_person = scrapy.Field()

    accusationType = scrapy.Field()
    sentence = scrapy.Field()
    releaseDate = scrapy.Field()
    servingPlace = scrapy.Field()
    dangerEstimateType = scrapy.Field()
    connectDate = scrapy.Field()
    connectCondition = scrapy.Field()
    settleDate = scrapy.Field()
    settleCondition = scrapy.Field()
    unsettleReason = scrapy.Field()
    educate = scrapy.Field()
    isRecidivist = scrapy.Field()
    isRepeat = scrapy.Field()

class BasebuildingItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    #idcard = scrapy.Field()
    #name_person = scrapy.Field()
    name = scrapy.Field()
    floor = scrapy.Field()
    code = scrapy.Field()
    address = scrapy.Field()

class CommunityItem(scrapy.Item):

    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idcard = scrapy.Field()
    name = scrapy.Field()

    rectificationType = scrapy.Field()
    caseType = scrapy.Field()
    specificAccusation = scrapy.Field()
    receiveWay = scrapy.Field()
    rectificationStart = scrapy.Field()
    rectificationEnd = scrapy.Field()

class CauseTroubleItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idcard = scrapy.Field()
    name = scrapy.Field()

    guardianName = scrapy.Field()
    guardianContact = scrapy.Field()
    diagnosisType = scrapy.Field()
    dangerEstimateLevel = scrapy.Field()
    cure = scrapy.Field()



class DrugItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idcard = scrapy.Field()
    name = scrapy.Field()

class KeypersonItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idcard = scrapy.Field()
    name = scrapy.Field()

    interviewReason = scrapy.Field()
    officialsName = scrapy.Field()
    chargeName = scrapy.Field()
    visitNum = scrapy.Field()

class EnterpriseItem(scrapy.Item):

    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    type = scrapy.Field()
    enterpriseType = scrapy.Field()
    contact = scrapy.Field()
    name = scrapy.Field()
    corAddr = scrapy.Field()
    respoName = scrapy.Field()


class OrganizationItem(scrapy.Item):

    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    type = scrapy.Field()
    organizationType = scrapy.Field()

    name = scrapy.Field()
    aim = scrapy.Field()


class InstitutionItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    institutionName = scrapy.Field()
    institutionType = scrapy.Field()
    institutionLevel = scrapy.Field()

class InstitutionTeamItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    institutionId = scrapy.Field()
    phone = scrapy.Field()
    administrationLevel = scrapy.Field()
    name = scrapy.Field()
    idCard = scrapy.Field()
    born = scrapy.Field()
    sexStr = scrapy.Field()

class DefenseOrgItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    organizationName = scrapy.Field()
    organizationType = scrapy.Field()
    mainFunc = scrapy.Field()
    manager = scrapy.Field()
    teamTypeStr = scrapy.Field()

class DefenseTeamItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    institutionId = scrapy.Field()
    phone = scrapy.Field()
    administrationLevel = scrapy.Field()
    name = scrapy.Field()
    idCard = scrapy.Field()
    born = scrapy.Field()
    sexStr = scrapy.Field()

class CentItem(scrapy.Item):
    region_no = scrapy.Field()
    crawl_type = scrapy.Field()

    idCard = scrapy.Field()
    centerName = scrapy.Field()
    centerContact = scrapy.Field()
    chargeName = scrapy.Field()
    address = scrapy.Field()
    centerLevel = scrapy.Field()



























