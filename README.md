# News Aggregator with Sentiment Analysis
A web application that aggregates news articles based on user-inputted search queries and categorizes them using sentiment analysis. This project integrates news aggregation with natural language processing (NLP) to provide a user-friendly platform for browsing personalized news with visual sentiment indicators.

## Table of Contents
  [## Features](features)
  
  [Technologies Used](technologies-used)
  
  [Installation](installation)
  
  [Usage](usage)
  
  [Project Structure](project-structure)
  
  [Screenshots](screenshots)

  [Future Improvements](future-improvements)

## Features
Fetches real-time news articles using SerpApi.

Provides sentiment analysis for news snippets (positive, negative, or neutral).

Color-coded sentiment visualization for easy interpretation.
User-friendly interface with pagination for large datasets.
Search functionality to filter news based on user queries.

## Technologies Used
Backend: Python, Django
Frontend: HTML, CSS, Bootstrap
API Integration: SerpApi - Google News API
Sentiment Analysis: VADER or TextBlob
Deployment: Render (Free tier)

## Installation
1. ### Prerequisites
   
- Python 3.8 or higher
- Django (latest compatible version)
- Pip package manager
- API key for SerpApi
  
2. ### Clone the Repository
```
git clone https://github.com/yourusername/news-aggregator-sentiment-analysis.git
cd news-aggregator-sentiment-analysis
```
3. ### Set Up a Virtual Environment
```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
4. ### Install Dependencies
```
pip install -r requirements.txt
```
5. ### Add Your API Key
Create a .env file in the root directory.
Add the following line to your .env file:
env
```
SERP_API_KEY=your_api_key_here
```
6. ### Run Database Migrations
```
python manage.py migrate
```
8. ### Collect Static Files
```
python manage.py collectstatic
```
9. ### Run the Server
```
python manage.py runserver
Access the app at http://127.0.0.1:8000/.
```

## Usage
1. Open the application in your browser.
2. Enter a keyword in the search bar (e.g., "technology" or "sports") and click Search.
3. Browse through the results, with each article color-coded by sentiment:
    - Green: Positive sentiment
    - Red: Negative sentiment
    - Blue: Neutral sentiment
4. Use the pagination controls to navigate through the results.

## Project Structure
```
├── aggregator/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         # Custom styles for the app
│   ├── templates/
│   │   ├── aggregator/
│   │   │   ├── about.html        # About page
│   │   │   ├── news_list.html    # Results display page
│   │   │   └── search.html       # Search input page
│   ├── views.py                  # Core logic for API integration and sentiment analysis
│   ├── urls.py                   # URL routing for the app
├── manage.py
├── requirements.txt              # Project dependencies
├── Procfile                      # Config for deployment
├── README.md                     # Documentation'''
```

## Screenshots
### Homepage
![image](https://github.com/user-attachments/assets/4cc23c8e-dc75-4194-a710-a13e13e50291)

### Search Results
![image](https://github.com/user-attachments/assets/0d724832-c855-4e17-8d6c-19074571737b)

## Future Improvements
- Advanced Sentiment Analysis: Incorporate transformer-based models like BERT for improved accuracy.
- User Accounts: Allow users to save preferences or search history.
- Multi-Language Support: Add support for non-English news articles.
- Enhanced Filtering: Provide options to filter news by source or date range.
