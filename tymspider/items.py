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




