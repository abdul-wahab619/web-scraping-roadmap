import os
import base64
import scrapy
from dotenv import load_dotenv

load_dotenv()


class AuthSpider(scrapy.Spider):
    name = "auth"
    allowed_domains = ["httpbin.org"]

    async def start(self):
        username = os.getenv("SCRAPER_USERNAME")
        password = os.getenv("SCRAPER_PASSWORD")

        credentials = f"{username}:{password}"
        encoded = base64.b64encode(credentials.encode()).decode()

        auth_header = f"Basic {encoded}"

        yield scrapy.Request(
            f"https://httpbin.org/basic-auth/{username}/{password}",
            headers={"Authorization": auth_header},
            callback=self.parse,
        )

    def parse(self, response):
        print("STATUS:", response.status)
        print("SERVER RESPONSE:")
        print(response.text)
