import scrapy


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["quotes.toscrape.com"]

    async def start(self):
        yield scrapy.Request(
            "https://quotes.toscrape.com/login",
            callback=self.parse_login,
        )

    def parse_login(self, response):
        print("LOGIN PAGE STATUS:", response.status)

        csrf_token = response.xpath("//input[@name='csrf_token']/@value").get()

        print("CSRF TOKEN:", csrf_token)

        yield scrapy.FormRequest(
            url="https://quotes.toscrape.com/login",
            formdata={
                "csrf_token": csrf_token,
                "username": "abdul",
                "password": "test123",
            },
            callback=self.after_login,
        )

    def after_login(self, response):
        print("LOGIN RESPONSE STATUS:", response.status)
        print("CURRENT URL:", response.url)

        logout_link = response.xpath("//a[@href='/logout']/text()").get()

        if logout_link:
            print("LOGIN SUCCESS: authenticated session detected")
        else:
            print("LOGIN FAILED: authenticated session not detected")
