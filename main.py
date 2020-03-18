from aws_textract import aws_textract
from web_scraper import web_scraper

awstextract = aws_textract()
scraper = web_scraper()
scanned_label = awstextract.main("wine-analyzer","hoya.jpg")
wine_info = scraper.get_wine_info(scanned_label)
print(wine_info)