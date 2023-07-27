from django.shortcuts import render
from django.http import HttpResponse
import os
import requests
from django.core.paginator import Paginator

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
            
