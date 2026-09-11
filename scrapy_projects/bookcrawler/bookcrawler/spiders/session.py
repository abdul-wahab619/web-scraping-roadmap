import scrapy


class SessionSpider(scrapy.Spider):
    name = "session"
    allowed_domains = ["httpbin.org"]

    async def start(self):
        yield scrapy.Request(
            "https://httpbin.org/cookies/set/session_id/abc123",
            callback=self.after_login,
        )

    def after_login(self, response):
        print("SESSION CREATED")

        yield scrapy.Request(
            "https://httpbin.org/cookies", callback=self.check_session, dont_filter=True
        )

    def check_session(self, response):
        print("SESSION RESPONSE:")
        print(response.text)

        yield scrapy.Request(
            "https://httpbin.org/cookies",
            callback=self.check_session_again,
            dont_filter=True,
        )

    def check_session_again(self, response):
        print("SECOND SESSION RESPONSE:")
        print(response.text)
