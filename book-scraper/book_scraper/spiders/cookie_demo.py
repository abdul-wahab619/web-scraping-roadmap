import scrapy
import os
from urllib.parse import urlsplit, quote
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class CookieDemoSpider(scrapy.Spider):
    name = "cookie_demo"
    allowed_domains = ["httpbin.org"]

    custom_settings = {
        "ITEM_PIPELINES": {},
        "SPIDERMON_ENABLED": False,
        "EXTENSIONS": {
            "spidermon.contrib.scrapy.extensions.Spidermon": None,
        },
        "HTTPPROXY_ENABLED": True,
        "FEED_EXPORT_FIELDS": ["test", "cookies"],
        "FEEDS": {
            "exports/cookie_test.jsonl": {
                "format": "jsonlines",
                "encoding": "utf8",
                "overwrite": True,
            },
        },
    }

    def get_proxy_meta(self, cookiejar):
        proxy_url = os.getenv("SCRAPY_PROXY_URL")
        proxy_user = os.getenv("SCRAPY_PROXY_USER")
        proxy_password = os.getenv("SCRAPY_PROXY_PASSWORD")

        if not all([proxy_url, proxy_user, proxy_password]):
            raise ValueError("Proxy configuration is missing from .env")

        return {
            "cookiejar": cookiejar,
            "proxy": proxy_url,
            "proxy_auth": (proxy_user, proxy_password),
        }

    def get_proxy_url(self):
        proxy_url = os.getenv("SCRAPY_PROXY_URL")
        proxy_user = os.getenv("SCRAPY_PROXY_USER")
        proxy_password = os.getenv("SCRAPY_PROXY_PASSWORD")

        if not all([proxy_url, proxy_user, proxy_password]):
            raise ValueError("Missing proxy configuration in .env")

        parsed = urlsplit(proxy_url)

        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or not parsed.port
        ):
            raise ValueError("Invalid proxy URL")

        username = quote(proxy_user, safe="")
        password = quote(proxy_password, safe="")

        return (
            f"{parsed.scheme}://{username}:{password}"
            f"@{parsed.hostname}:{parsed.port}"
        )

    async def start(self):
        mode = getattr(self, "mode", "cookies")

        if mode == "status_test":
            yield scrapy.Request(
                "https://httpbin.org/status/403",
                callback=self.parse_status,
                meta={
                    "proxy": self.get_proxy_url(),
                    "dont_retry": True,
                    "handle_httpstatus_all": True,
                },
            )
            return

        yield scrapy.Request(
            "https://httpbin.org/cookies/set/session_id/scrapy_demo",
            callback=self.parse,
            meta={
                "cookiejar": "session_1",
                "proxy": self.get_proxy_url(),
            },
        )

    def parse_status(self, response):
        self.logger.info(
            "Status test completed: HTTP %s received from %s",
            response.status,
            response.url,
        )

    def parse(self, response):
        yield scrapy.Request(
            "https://httpbin.org/cookies?verify=1",
            callback=self.check_cookies,
            meta={
                "cookiejar": response.meta["cookiejar"],
                "proxy": self.get_proxy_url(),
            },
        )

    def check_cookies(self, response):
        cookies = response.json().get("cookies", {})

        self.logger.info("Cookies received: %s", cookies)

        yield {
            "test": "cookie_session",
            "cookies": cookies,
        }
