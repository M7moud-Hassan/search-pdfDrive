from bs4 import BeautifulSoup
import requests

from .models import Book,Keyword


base_url="https://www.pdfdrive.com/search?q={0}&page={1}"

def search(keyword):
    numPages=1
    response = requests.get(base_url.format(keyword,1))
    if response.status_code==200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination_div = soup.find('div', class_='Zebra_Pagination')
        keyword_=Keyword.objects.create(name=keyword)
        if pagination_div:
            
            li_elements = pagination_div.find_all('li')
            if len(li_elements) > 2:
                second_to_last_li = li_elements[-2]
                numPages=int(second_to_last_li.get_text(strip=True))
        for page_number in range(1, numPages):    
                add_pagination(keyword,page_number,keyword_)
                

def add_pagination(keyword,numPge,keyword_):
    response = requests.get(base_url.format(keyword,numPge))
    if response.status_code==200:
        soup = BeautifulSoup(response.text, 'html.parser')
        files_new_div = soup.find('div', class_='files-new')
        if files_new_div:
            li_elements = files_new_div.find_all('li')     
            for li in li_elements:
                img = li.find('img', class_='img-zoom')
                img_src = img['data-original']
                ai_search = li.find('a', {'class':'ai-search'}).text.strip()
                fi_year = li.find('span', {'class':'fi-year'}).text.strip()
                fi_size = li.find('span', {'class':'fi-size hidemobile'}).text.strip()
                file_info = li.find('div', {'class':'file-info'}).text.strip()
                book, created = Book.objects.get_or_create(address=ai_search, description=file_info,image=img_src,
                                                        year=fi_year,size=fi_size,defaults={'address': ai_search})
                keyword_.books.add(book)
                