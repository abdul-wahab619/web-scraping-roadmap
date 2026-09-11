import scrapy


class CookiesSpider(scrapy.Spider):
    name = "cookies"
    allowed_domains = ["httpbin.org"]

    async def start(self):
        yield scrapy.Request(
            "https://httpbin.org/cookies/set/session_id/abc123",
            callback=self.after_cookie,
        )

    def after_cookie(self, response):
        print("FIRST RESPONSE:", response.status)

        yield scrapy.Request(
            "https://httpbin.org/cookies", callback=self.parse, dont_filter=True
        )

    def parse(self, response):
        print("SERVER RESPONSE:")
        print(response.text)
