from icrawler.builtin import GoogleImageCrawler

google_crawler = GoogleImageCrawler(storage={"root_dir": "./images"})
google_crawler.crawl(keyword="zelda", max_num=1)
