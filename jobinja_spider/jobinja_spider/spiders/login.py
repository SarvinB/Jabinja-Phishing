import scrapy
from urllib.parse import urlparse
import os

class JobinjaSpider(scrapy.Spider):
    
    name = "login"
    handle_httpstatus_all = True   

    async def start(self):
        
        self.visited = set()
        self.start_urls = ["https://jobinja.ir/"]
        self.allowed_domain = "jobinja.ir"
        
        yield scrapy.Request(
            "https://jobinja.ir/login/user",
            callback=self.login_page,
            meta={
                "identifier": "sarvin80.b@gmail.com",
                "password": "13802001",
            }
        )

    def login_page(self, response):
        
        print("ok")
        csrf = response.css(
            'input[name="_token"]::attr(value)'
        ).get()

        yield scrapy.FormRequest(
            url="https://jobinja.ir/login/user",
            formdata={
                "identifier": response.meta["identifier"],
                "password": response.meta["password"],
                "_token": csrf,
            },
            headers={
                "Referer": "https://jobinja.ir/login/user",
                "X-Requested-With": "XMLHttpRequest",
            },
            callback=self.extract_pages,
            dont_filter=True
        )

    def extract_pages(self, response):
        
        # print("ok")

        current_url = response.url

        # جلوگیری از بازدید دوباره
        # if current_url in self.visited:
        #     return
        
        # self.visited.add(current_url)

        # self.visited.add(current_url)

        # self.logger.info(f"Visiting: {current_url}")

        # # استخراج لینک‌ها
        links = response.css("a::attr(href)").getall()
        
        print("STATUS:", response.status)
        print("URL:", response.url)
    
        yield {
            "url": current_url,
            "html": response.text
        }

        for link in links:
            
            if "companies" in link or "jobs?filters" in link or "recover?" in link or "auth" in link or "telegram" in link or "logout" in link or "redirect" in link:
                # print(link)
                continue
            
            if "{{" in link or "}}" in link:
                continue

            if not link or link.strip() == "#":
                continue
            
            
            absolute = response.urljoin(link)

            parsed = urlparse(absolute)

            # فقط لینک‌های داخلی
            if parsed.netloc == self.allowed_domain:
                
                # رفتن به صفحه بعد
                # if absolute not in self.visited:
                    
                #     print("********", absolute)

                    
                yield scrapy.Request(
                    absolute,
                    callback=self.extract_pages,
                    errback=self.handle_error,
                    dont_filter=False 
                )
        
        # folder_path = "/Users/sarvinbaghi/Desktop/Codes/Cyber Security/JobBinja/flask_login_demo/templates"
        # filename = current_url + '.html'

        # # Combine them
        # full_path = os.path.join(folder_path, filename)
        
        # with open(full_path, 'w', encoding='utf-8') as file:
        #     file.write(response.text)

                    
        # print(current_url[:40])
        # ذخیره نتیجه


        
    def handle_error(self, failure):
        self.logger.error(repr(failure))