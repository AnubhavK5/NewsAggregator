# from transformers import pipeline
from textblob import TextBlob
from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from django.http import HttpResponse
from django.http import JsonResponse

# Lazy-load the sentiment analysis model
# def get_sentiment_analyzer():
#     return pipeline(
#         "sentiment-analysis",
#         model="distilbert-base-uncased-finetuned-sst-2-english"
#     )

# def analyze_sentiment(text):
#     sentiment_analyzer = get_sentiment_analyzer()
#     return sentiment_analyzer(text)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


def home(request):
    return render(request, 'aggregator/search.html', {'title': 'news_home'})

def fetch_news(request):
    api_key = '266d5581b408f4932846c2caeb99223efd98dd5c807de1838655b4716dbe1e3d' 
    api_url = 'https://serpapi.com/search.json'

    query = request.GET.get('query', '').strip()

    if not query:
        # If no query is provided, render the search page
        return render(request, 'aggregator/search.html')
   

    # Parameters for the API request
    params = {
        'q': query,  # Search query for latest news
        'tbm': 'nws',        # Search type: news
        'location': 'India',  # Location filter (adjust as needed)
        'api_key': api_key,  # SerpApi key
    }

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        news_data = response.json()
      

        # Process the news results
        filtered_articles = []
        for article in news_data.get('news_results', []):
            title = article.get('title')
            link = article.get('link')
            snippet = article.get('snippet')
            thumbnail = article.get('thumbnail')

            # Include articles with all required fields
            if title and snippet and link and thumbnail:
                sentiment_label = analyze_sentiment(snippet+title)

                filtered_articles.append({
                    'title': title,
                    'description': snippet,
                    'urlToImage': thumbnail,
                    'url': link,
                    'sentiment': sentiment_label,
                })

        # Paginate the articles
        paginator = Paginator(filtered_articles, 16)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        return render(request, 'aggregator/news_list.html',{'page_obj': page_obj, 'query': query})

    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return render(request, 'aggregator/news_list.html', {'page_obj': None, 'error': 'Failed to fetch news.'})

def about(request):
    return render(request, "aggregator/about.html", {'title': 'About'})




