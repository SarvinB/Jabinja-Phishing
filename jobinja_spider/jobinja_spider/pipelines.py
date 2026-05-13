# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from urllib.parse import quote


class JobinjaSpiderPipeline:
    
    def process_item(self, item, spider):
        
        safe_name = quote(item["url"], safe="")
        path = "/Users/sarvinbaghi/Desktop/Codes/Cyber Security/JobBinja/flask_login_demo/templates"

        os.makedirs(path, exist_ok=True)
        
        file_path = os.path.join(path, safe_name + ".html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(item["html"])

        return item
