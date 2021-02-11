from bs4 import BeautifulSoup
import numpy as np
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def superScraper(keyword):
  job_titles = []
  company_names = []
  apply_urls = []

  def bsRequests(url):
    html = requests.get(url,headers=headers).text
    bs = BeautifulSoup(html,'html.parser')
    return bs

  def scrapeStackoverflow():
    pg_num = 1
    url = f'https://stackoverflow.com/jobs?r=true&q={keyword}&pg={pg_num}'
    url_head = 'https://stackoverflow.com'
    
    stackoverflow_bs = bsRequests(url)
    try:
      page_num = len(stackoverflow_bs.find('div',class_='s-pagination').find_all('a'))-1
    except:
      page_num = 1
    
    for howmany in range(page_num):
      stackoverflow_bs = bsRequests(url)
      search_results = stackoverflow_bs.find('div',class_='listResults')
      for content in search_results.find_all('h2'):
        try:
          job_titles.append(content.find('a').text)
          apply_urls.append(url_head+content.find('a')['href'])
        except:
          pass
      for co_name in search_results.find_all('h3'):
        company_names.append(co_name.find('span').text.strip())
          
      pg_num+=1
      url = f'https://stackoverflow.com/jobs?r=true&q={keyword}&pg={pg_num}'

  def scrapeWeworkremotely():
    url = f'https://weworkremotely.com/remote-jobs/search?term={keyword}'
    url_head = 'https://weworkremotely.com'
    weworkremotely_bs = bsRequests(url)
    search_results = weworkremotely_bs.select('section.jobs article ul li a')
    for content in search_results:
      apply_url = content['href']
      company_name = content.find('span',class_='company')
      job_title = content.find('span',class_='title')
      if (apply_url.startswith('/remote-jobs/') and all(v is not None for v in [company_name,job_title])):
        job_titles.append(job_title.text)
        company_names.append(company_name.text)
        apply_urls.append(url_head+apply_url)
  
  def scrapeRemoteok():
    url = f'https://remoteok.io/remote-{keyword}-jobs'
    url_head = 'https://remoteok.io'
    remoteok_bs = bsRequests(url)
    search_results = remoteok_bs.select('table tr.job')
    for content in search_results:
      job_titles.append(content.find('h2').text)
      company_names.append(content['data-company'])
      apply_urls.append(url_head+content['data-href'])

  # stackoverflow scraper
  scrapeStackoverflow()
  # weworkremotely scraper
  scrapeWeworkremotely()
  # remoteok scraper
  scrapeRemoteok()

  full_results = np.column_stack((job_titles,company_names,apply_urls)).tolist()

  return full_results