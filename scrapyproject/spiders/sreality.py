from scrapyproject.items import ScrapyprojectItem  

import scrapy

class SrealitySpider(scrapy.Spider):
    name = "sreality"
    allowed_domains = ["scrapeme.live"]
    start_urls = ["https://scrapeme.live/shop/"] # Did not use sreality.cz because of robots.txt having: User-agent: * Disallow: /
    
    count = 0
    max_items = 500

    def start_requests(self):
        url = 'https://scrapeme.live/shop/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = ScrapyprojectItem()
        for product in response.css('li.product'):
            item['title'] = product.css('h2.woocommerce-loop-product__title::text').get()
            item['image_url'] = product.css('img.attachment-woocommerce_thumbnail::attr(src)').get()
            yield item
            self.count += 1
            if self.count >= self.max_items:
                self.log(f'Reached maximum item limit of {self.max_items}. Stopping spider.')
                return
        
        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)