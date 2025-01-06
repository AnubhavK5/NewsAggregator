from transformers import pipeline
from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from django.http import HttpResponse
from django.http import JsonResponse

# Lazy-load the sentiment analysis model
def get_sentiment_analyzer():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

def analyze_sentiment(text):
    sentiment_analyzer = get_sentiment_analyzer()
    return sentiment_analyzer(text)

def fetch_news(request):
    api_key = 'f0e342ac1b704a28b10a9bf6776fc51f'  # Replace with your API key
    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        news_data = response.json()

        # Filter out articles without required fields
        filtered_articles = []
        for article in news_data.get('articles', []):
            if article.get('title') and article.get('description') and article.get('urlToImage'):
                # Perform sentiment analysis on the description
                sentiment_result = analyze_sentiment(article['description'])[0]
                sentiment_label = sentiment_result['label'].lower()

                # Map sentiment labels
                if sentiment_label == 'positive':
                    article['sentiment'] = 'positive'
                elif sentiment_label == 'negative':
                    article['sentiment'] = 'negative'
                else:
                    article['sentiment'] = 'neutral'

                filtered_articles.append(article)

        # Paginate the articles
        paginator = Paginator(filtered_articles, 16)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        return render(request, 'aggregator/news_list.html', {'page_obj': page_obj})

    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return render(request, 'aggregator/news_list.html', {'page_obj': None, 'error': 'Failed to fetch news.'})

def about(request):
    return render(request, "aggregator/about.html", {'title': 'About'})