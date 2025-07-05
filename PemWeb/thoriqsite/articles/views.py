# articles/views.py
from django.shortcuts import render, get_object_or_404 # Tambahkan get_object_or_404
from .models import Article 

def article_list_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/article_list.html', context)

# TAMBAHKAN VIEW BARU DI BAWAH INI
def article_detail_view(request, pk):
    """
    Menampilkan satu artikel secara spesifik berdasarkan Primary Key (pk).
    """
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/article_detail.html', context)