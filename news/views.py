from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
import os
import requests
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import DetailView

# Create your views here.
def home(request):
    api = os.environ.get("news_api")
    url = "https://newsapi.org/v2/everything?q={}&sortBy=popularity&apiKey={}"


    if request.method == "POST":

        search_term = request.POST['search']
        articles = fetch_news_data(url, search_term, api)

        p = Paginator(articles, 5)
        page_number = request.POST.get("page")
        article_new = p.get_page(page_number)

        context = {
            # "articles": articles,
            "article_new": article_new,
        }

        return render(request, "news/home.html", context)
    else:
        return render(request, "news/home.html")



# Class based view
class NewsList(View):
    api = os.environ.get("news_api")
    url = "https://newsapi.org/v2/everything?q={}&sortBy=popularity&apiKey={}"
    template = "news/home.html"
    # context_object_name = "article_new"

    def get(self, request):
        search_term = request.GET.get('search')
        articles = fetch_news_data(self.url, search_term, NewsList.api)

        p = Paginator(articles, 5)
        page_number = request.GET.get("page")
        article_new = p.get_page(page_number)

        context = {
            # "articles": articles,
            "article_new": article_new,
        }

        return render(request, "news/home.html", context)
    

class NewsDetail(DetailView, NewsList):
    template_name = "news/detail.html"
    slug_url_kwarg = "title"
    slug_field = "title"
    context_object_name = "article"
    # api = os.environ.get("news_api")
    # url = "https://newsapi.org/v2/everything?q={}&sortBy=popularity&apiKey={}"

    def get_object(self, queryset=  None):
        title = self.kwargs.get(self.slug_url_kwarg)
        articles = fetch_news_data(self.url, self.search_term, NewsList.api)

        for article in articles:
            if article["title"] == title:
                return article
            
        return None
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


def redirect_to_detail(request, title):
    articles = fetch_news_data(url, search_term, api)



# Function to fetch and return the news data 
def fetch_news_data(url, search_term, api):
    response = requests.get(url.format(search_term, api)).json()
  
    news_articles = []
    for article in response["articles"][:50]:
        news_articles.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "imageUrl": article["urlToImage"],
            "published_at": article["publishedAt"],
            "content": article["content"],
            "author": article["author"],
            "magazine": article["source"]["name"]
        })

    return news_articles
            
