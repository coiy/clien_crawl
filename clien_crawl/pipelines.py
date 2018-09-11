from pymongo import MongoClient 

class MongoPipeline(object):
    """
    Item을 MongoDB에 저장하는 Pipeline
    """
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['scrap_clien']
        self.collection = self.db['article']
    
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))    

