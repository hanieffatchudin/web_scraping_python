#request Html page
import requests
import pprint
import datetime
import nltk
from scrapy import Selector
from nltk.corpus import stopwords
from collections import Counter
nltk.download('punkt')
nltk.download('stopwords')

pp = pprint.PrettyPrinter(indent=2)

response = requests.get("https://www.pikiran-rakyat.com/jawa-barat")
html_page = response.content
html_sel = Selector(text=html_page)

new_url = html_sel.css("div.latest__item>div> h2 > a::attr(href)").extract()
news_url = new_url[0:10]

#looping
data_fixs = []

for a in news_url:
  data_sementara = {}
  #datetime now
  x = datetime.datetime.now()
  data_sementara['scrape_time'] = x.strftime("%Y-%m-%d %H:%M:%S")
  
  #url to selector
  nu = requests.get(a)
  nu_page = nu.content
  nu_sel = Selector(text=nu_page)

  #datetime release 
  datetimes=nu_sel.css("div.read__info__date")
  data_sementara["story_release_date"] = datetimes.css("::text").extract_first().translate(str.maketrans('', '', '\n-')).strip()

  #source
  source=nu_sel.css("p:nth-child(2) > strong")
  data_sementara["story_source"] = source.css("::text").extract_first()#.translate(str.maketrans('', '', '-\xa0')).strip()

  #title
  title=nu_sel.css("div > h1")
  data_sementara["story_title"] = title.css("::text").extract_first()

  #url
  data_sementara['story_url'] = a

  #most commond word
  #page1
  most=nu_sel.css("div.col-bs12-9 > article")
  timework = most.css("::text").extract()
  content1 =''.join(timework).translate(str.maketrans('', '', '\n-\xa0.,?();:"\{}')).strip()

  #page2
  nus = requests.get(a + '?page=2')
  nus_page = nus.content
  nus_sel = Selector(text=nus_page)

  mosts=nus_sel.css("div.col-bs12-9 > article")
  timeworks = most.css("::text").extract()
  content2 = ''.join(timeworks).translate(str.maketrans('', '', '\n-\xa0.,?();:"\{}')).strip()

  #nltk
  nltk_tokens = nltk.word_tokenize(content1+content2)

  #stop words
  id_stops = set(stopwords.words('indonesian'))

  kata = []
  for word in nltk_tokens: 
    if word not in id_stops:
      kata.append(word)
    
  #Counter word
  counter = Counter(kata)
  most_occur = counter.most_common(5)
  
  
  data_sementara["most_common_words"] = most_occur

  data_fixs.append(data_sementara)