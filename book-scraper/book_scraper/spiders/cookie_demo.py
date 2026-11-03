import scrapy


class CookieDemoSpider(scrapy.Spider):
    name = "cookie_demo"
    allowed_domains = ["httpbin.org"]

    # This demonstration should not write test data to PostgreSQL
    # or run the 100-book Spidermon check.
    custom_settings = {
        "ITEM_PIPELINES": {},
        "SPIDERMON_ENABLED": False,
        "EXTENSIONS": {
            "spidermon.contrib.scrapy.extensions.Spidermon": None,
        },
    }

    async def start(self):
        yield scrapy.Request(
            "https://httpbin.org/cookies/set/session_id/scrapy_demo",
            callback=self.parse,
            meta={"cookiejar": "session_1"},
        )

    def parse(self, response):
        yield scrapy.Request(
            "https://httpbin.org/cookies?verify=1",
            callback=self.check_cookies,
            meta={
                "cookiejar": response.meta["cookiejar"],
            },
        )

    def check_cookies(self, response):
        cookies = response.json().get("cookies", {})

        self.logger.info("Cookies received: %s", cookies)

        yield {
            "test": "cookie_session",
            "cookies": cookies,
        }
