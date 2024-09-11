from django.shortcuts import render, get_object_or_404
from .models import NewsArticle

def news_list(request):
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    newspaper_filter = request.GET.get('newspaper', '')

    articles = NewsArticle.objects.all()

    if query:
        articles = articles.filter(title__icontains=query)
    if date_filter:
        articles = articles.filter(date=date_filter)
    if newspaper_filter:
        articles = articles.filter(newspaper_name=newspaper_filter)

    context = {
        'articles': articles
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk)
    context = {
        'article': article
    }
    return render(request, 'news/news_detail.html', context)
