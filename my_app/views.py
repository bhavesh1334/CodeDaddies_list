import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models


# BASE_CRAGLIST_URL = 'https://kolkata.craigslist.org/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
BASE_CRAGLIST_URL='https://losangeles.craigslist.org/search/hhh?query={}'
# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup= BeautifulSoup(data, features='html.parser')
    
    post_listings = soup.find_all('li', class_ = 'result-row')
    # post_title = post_listings[1].find(class_ = 'result-title').text
    # post_url = post_listings[1].find('a').get('href')
    # post_price = post_listings[1].find(class_ = 'result-price').text
    
    # print('TITLE:',post_title)
    # print('POST_URL:',post_url)
    # print('PRICE:',post_price)
    # print(post_listings)
    final_postings=[]

    for post in post_listings:
        post_title= post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        
        if post.find(class_='result-price'):
            post_price=post.find(class_='result-price').text
        else:
            post_price='N/A'       

        if post.find(class_='result-image').get('data-ids'):
            post_image_id= post.find(class_='result-image').get('data-ids').split(',')[0].split(':')
            post_image_url=BASE_IMAGE_URL.format(post_image_id[1])
            print(post_image_url)
        else:
            post_image_url='https://craigslist.org/images/peace.jpg'        
        
        
        final_postings.append((post_title,post_url,post_price,post_image_url))
        
    
    # post_titles= soup.find_all('a',{'class':'result-title'})
    # print(post_titles[0].text)
    #print(data)
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings ,
    }
    
    return render(request, 'my_app/new_search.html',stuff_for_frontend)