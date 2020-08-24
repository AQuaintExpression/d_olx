from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from . import models

BASE_OLX_URL = "https://www.olx.ro/oferte/q-{}/?search%5Bphotos%5D=1"


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    search_url = BASE_OLX_URL.format('-'.join(search.split()))
    data = requests.get(search_url)
    soup = BeautifulSoup(data.text, features='html.parser')
    posts = soup.find_all('div', {'class':'offer-wrapper'})

    # print('*\n'*8)
    # print(soup.find_all('div', {'class': 'emptynew'}))
    # print('*\n' * 8)

    #todo check if something was found

    final_posts = []
    for post in posts:
        # print('*' * 8 + '\n\n\n\n' + str(len(posts)) + '\n\n\n\n' + '*' * 8)
        post_title = post.find('a', {'data-cy': 'listing-ad-title'}).text.strip()
        post_url = post.find('a', {'data-cy': 'listing-ad-title'}).attrs['href']
        post_image = post.find('img', {'class': "fleft"}).attrs['src']
        post_price = post.find('div', {'class':"space inlblk rel"}).text.strip()

        final_posts.append((post_title, post_image, post_url, post_price))

    print(final_posts)

    stuff_for_frontend = {
        'search': search,
        'final_posts': final_posts,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
