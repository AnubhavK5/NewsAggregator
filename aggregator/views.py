from transformers import pipeline
from django.shortcuts import render
from django.core.paginator import Paginator
import requests
from django.http import HttpResponse
from django.http import JsonResponse

sentiment_analyzer = pipeline("sentiment-analysis", model='distilbert/distilbert-base-uncased-finetuned-sst-2-english',
    revision='714eb0f')

def fetch_news(request):
    api_key = 'f0e342ac1b704a28b10a9bf6776fc51f' 
    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    # https://newsapi.org/v2/top-headlines?country=in&apiKey=f0e342ac1b704a28b10a9bf6776fc51f
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors
        news_data = response.json()
        # print(news_data)

        # Filter out articles without title, description, or image
        filtered_articles = []
        for article in news_data.get('articles', []):
            if article.get('title') and article.get('description') and article.get('urlToImage'):
                # Perform sentiment analysis on the description
                sentiment_result = sentiment_analyzer(article['description'])[0]
                sentiment_label = sentiment_result['label'].lower()  # Convert to lowercase for consistency

                # Map labels to positive, negative, or neutral
                if sentiment_label == 'positive':
                    article['sentiment'] = 'positive'
                elif sentiment_label == 'negative':
                    article['sentiment'] = 'negative'
                else:
                    article['sentiment'] = 'neutral'

                filtered_articles.append(article)

        # Set up pagination: 16 articles per page
        paginator = Paginator(filtered_articles, 16)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Render the template with paginated articles
        return render(request, 'aggregator/news_list.html', {'page_obj': page_obj})

    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return render(request, 'aggregator/news_list.html', {'page_obj': None, 'error': 'Failed to fetch news.'})



def about(request):
    return render(request, "aggregator/about.html", {'title':'about'})