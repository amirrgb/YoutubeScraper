import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import QuotestutorialItem ### .. means go to parent directory
import scrapy_user_agents


class quotesSpider(scrapy.Spider):
    name = "quotes"  ### this should be unique

    start_urls = ['https://quotes.toscrape.com/login']  ### this is start urls list will be parsed

    def parse(self, response):  ### response is pagesource of url
        # title = response.css('title').extract()  ### return a list
        # for i in title:
        #     i.get()  ### we use get() to find elements in ohter elements
        # title = response.css('title').extract_first()  ### return a first matched item
        # title = response.css('title::text').extract()  ### (related to css selectors) this is the same as the above line but just text inside
        # yield {"titleText": title}  ### this will send it to itemsContainer in items.py file
        # filename = f'quotes-{page}.html' ### f'any {thing}String' means  put thing in {} (str.format)
        # with open(filename, 'wb') as f: ### 'wb' or other 'b' modes means open in binary mode
        #     f.write(response.body)   ### body means html file with all tags
        # self.log(f'Saved file {filename}')  ### i dont know what is that
        token = response.css('form input::attr(value)').extract_first()
        # print("\n\n\n\n\n\n>>>>>\n%s\n<<<<<\n\n\n\n\n"%token)
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': "salamuser",
            'password': "salampass"
        }, callback=self.start_scraper, dont_click=True)

    def start_scraper(self, response):
        items = QuotestutorialItem()

        all_div_quotes = response.css('div.quote')

        for quotes in all_div_quotes:
            title = quotes.css("span.text::text").extract()
            author = quotes.css(".author::text").extract()
            tag = quotes.css(".tag::text").extract()
            items['title'] = title
            items["author"] = author
            items["tag"] = tag
            yield items
        next_page = response.css("li.next a::attr(href)").get()
        self.log(">>>>>>>>>\n\n\nopening last page in browser")
        open_in_browser(response)
        if next_page is not None:
            yield response.follow(next_page,
                                  callback=self.start_scraper)  # for callback we use just method name without ()
        else:
            print("opening last page in browser")
            open_in_browser(response)  # its open last page in browser
