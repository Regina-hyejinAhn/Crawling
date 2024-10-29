import datetime
import re
import scrapy
import requests
from bs4 import BeautifulSoup

# Fetch the webpage
url = "https://arxiv.org/list/cs.AI/recent"
response = requests.get(url)
html_content = response.content

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find and extract data
title = soup.find("articles").text
paragraphs = [p.text for p in soup.find_all("p")]

print("Title:", title)
print("Paragraphs:", paragraphs)


class ArxivSpider(scrapy.Spider):
  name = "Arxiv"
  search_term = "Graph Neural Networks"
  search_term = search_term.replace(" ", "+")

  url = [f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=past_12&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first",]

def parset_out_html(self, string):
  string = string.strip().replace("\n", "").strip(' ')
  string = re.sub(r'<[^>]*>', '', string)
  string = string.strip()
  return string

def parse(self, response):
  for paper in response.css("li.arxiv-result"):
    title = paper.css("p.title").get()
    abstract = paper.css("p.abstract").css("span.abstract-full::text").get()
    submitted_date = paper.css("p.is-size-7::text").get().replace(';', '')
    yield {"title": self.parset_out_html(title),
           "abstract": self.parset_out_html(abstract),
           "submitted_date": self.parset_out_html(submitted_date),
           "scraped_time": datetime.datetime.now(),
          }
ArxivSpider




