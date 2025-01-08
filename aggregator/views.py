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

# def fetch_news(request):
#     api_key = 'f0e342ac1b704a28b10a9bf6776fc51f' 
#     api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         news_data = response.json()

#         # Filter out articles without required fields
#         filtered_articles = []
#         for article in news_data.get('articles', []):
#             if article.get('title') and article.get('description') and article.get('urlToImage'):
#                 # Perform sentiment analysis on the description
#                 sentiment_result = analyze_sentiment(article['description'])[0]
#                 sentiment_label = sentiment_result['label'].lower()

#                 # Map sentiment labels
#                 if sentiment_label == 'positive':
#                     article['sentiment'] = 'positive'
#                 elif sentiment_label == 'negative':
#                     article['sentiment'] = 'negative'
#                 else:
#                     article['sentiment'] = 'neutral'

#                 filtered_articles.append(article)

#         # Paginate the articles
#         paginator = Paginator(filtered_articles, 16)
#         page_number = request.GET.get('page', 1)
#         page_obj = paginator.get_page(page_number)

#         return render(request, 'aggregator/news_list.html', {'page_obj': page_obj})

#     except requests.RequestException as e:
#         print(f"Error fetching news: {e}")
#         return render(request, 'aggregator/news_list.html', {'page_obj': None, 'error': 'Failed to fetch news.'})

# def about(request):
#     return render(request, "aggregator/about.html", {'title': 'About'})




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
        'location': 'United States',  # Location filter (adjust as needed)
        'api_key': api_key,  # SerpApi key
    }

    try:
        response = requests.get(api_url, params=params)
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
                # Perform sentiment analysis
                sentiment_result = analyze_sentiment(snippet)[0]
                sentiment_label = sentiment_result['label'].lower()

                # Map sentiment labels
                if sentiment_label == 'positive':
                    sentiment = 'positive'
                elif sentiment_label == 'negative':
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'

                filtered_articles.append({
                    'title': title,
                    'description': snippet,
                    'urlToImage': thumbnail,
                    'url': link,
                    'sentiment': sentiment,
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




# def fetch_news(request):
#     api_key = 'your_bing_api_key'  # Replace with your Bing News API key
#     api_url = 'https://api.bing.microsoft.com/v7.0/news/search'

#     # Parameters for the API request
#     params = {
#         'q': 'latest news',  # Search query for the latest news
#         'count': 50,         # Number of articles to fetch
#         'mkt': 'en-US',      # Market for news
#         'safeSearch': 'Moderate',  # Filter inappropriate content
#     }

#     headers = {
#         'Ocp-Apim-Subscription-Key': api_key,  # Required Bing API header
#     }

#     try:
#         response = requests.get(api_url, headers=headers, params=params)
#         response.raise_for_status()
#         news_data = response.json()

#         # Process the news results
#         filtered_articles = []
#         for article in news_data.get('value', []):
#             title = article.get('name')
#             description = article.get('description')
#             url = article.get('url')
#             image = article.get('image', {}).get('thumbnail', {}).get('contentUrl')

#             # Include articles with all required fields
#             if title and description and url and image:
#                 # Perform sentiment analysis
#                 sentiment_result = analyze_sentiment(description)[0]
#                 sentiment_label = sentiment_result['label'].lower()

#                 # Map sentiment labels
#                 if sentiment_label == 'positive':
#                     sentiment = 'positive'
#                 elif sentiment_label == 'negative':
#                     sentiment = 'negative'
#                 else:
#                     sentiment = 'neutral'

#                 filtered_articles.append({
#                     'title': title,
#                     'description': description,
#                     'urlToImage': image,
#                     'url': url,
#                     'sentiment': sentiment,
#                 })

#         # Paginate the articles
#         paginator = Paginator(filtered_articles, 16)
#         page_number = request.GET.get('page', 1)
#         page_obj = paginator.get_page(page_number)

#         return render(request, 'aggregator/news_list.html', {'page_obj': page_obj})

#     except requests.RequestException as e:
#         print(f"Error fetching news: {e}")
#         return render(request, 'aggregator/news_list.html', {'page_obj': None, 'error': 'Failed to fetch news.'})

# def about(request):
#     return render(request, "aggregator/about.html", {'title': 'About'})