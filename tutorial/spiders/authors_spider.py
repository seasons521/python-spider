import scrapy

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for authorUrl in response.css(".author+a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(authorUrl), callback=self.parse_author_info)

        nextPage = response.css(".pager .next a::attr(href)").extract_first()
        if nextPage is not None:
            yield scrapy.Request(response.urljoin(nextPage), callback=self.parse)

    def parse_author_info(self, response):
        yield {
            'name': response.css(".author-title::text").extract_first(),
            'birth': response.css(".author-born-date::text").extract_first(),
            'location': response.css(".author-born-location::text").extract_first(),
            'description': response.css(".author-description::text").extract_first(),
        }

