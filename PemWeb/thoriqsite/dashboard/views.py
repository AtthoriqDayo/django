# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from articles.models import Article
from .forms import ArticleForm
import requests
import os
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile 
from urllib.parse import urlparse
from .forms import ArticleForm, UserUpdateForm # Update import form

@staff_member_required
def index_view(request):
    """ Tampilan utama dashboard """
    article_count = Article.objects.count()
    context = {
        'username': request.user.username,
        'article_count': article_count,
    }
    return render(request, 'dashboard/index.html', context)

@staff_member_required
def manage_articles_view(request):
    """ Halaman untuk melihat semua artikel (Read) """
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'dashboard/manage_articles.html', context)

@staff_member_required
def create_article_view(request):
    """ Halaman untuk menambah artikel baru (Create) """
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('dashboard:manage_articles')
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
        'form_title': 'Tambah Artikel Baru'
    }
    return render(request, 'dashboard/article_form.html', context)

@staff_member_required
def update_article_view(request, pk):
    """ Halaman untuk mengedit artikel (Update) """
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manage_articles')
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
        'form_title': 'Edit Artikel'
    }
    return render(request, 'dashboard/article_form.html', context)

@staff_member_required
def delete_article_view(request, pk):
    """ Halaman untuk menghapus artikel (Delete) """
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('dashboard:manage_articles')
    
    context = {
        'article': article
    }
    return render(request, 'dashboard/article_confirm_delete.html', context)

# dashboard/views.py

@staff_member_required
def import_news_view(request):
    """
    Mengambil berita dari GNews dan menampilkannya kepada admin.
    """
    selected_lang = request.GET.get('lang', 'id')

    # Menggunakan GNews API Key
    api_key = os.getenv('GNEWS_API_KEY') 
    
    # URL baru untuk GNews API
    # Perhatikan: parameter API key di GNews bernama 'token'
    url = f"https://gnews.io/api/v4/top-headlines?topic=technology&lang={selected_lang}&country=id&token={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles_from_api = data.get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from GNews: {e}")
        articles_from_api = []

    context = {
        'articles_from_api': articles_from_api,
        'selected_lang': selected_lang,
    }
    return render(request, 'dashboard/import_news.html', context)

# dashboard/views.py

# dashboard/views.py

@staff_member_required
def save_news_view(request):
    """
    Menyimpan artikel dari GNews, dengan penanganan konten yang pendek.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content_from_api = request.POST.get('content')
        source_url = request.POST.get('source_url')
        image_url = request.POST.get('image_url')

        # Logika baru untuk menangani konten pendek dari API
        # GNews sering memotong konten dan diakhiri dengan "[...]"
        if content_from_api and len(content_from_api) > 100: # Anggap konten valid jika lebih dari 100 karakter
             final_content = f"{content_from_api}<p class='mt-4'><em><strong>Artikel ini adalah ringkasan. Baca selengkapnya di <a href='{source_url}' target='_blank'>sumber asli</a>.</strong></em></p>"
        else:
             final_content = f"<p>Tidak ada ringkasan yang tersedia untuk artikel ini. Silakan kunjungi langsung sumbernya untuk membaca berita selengkapnya.</p><p><a href='{source_url}' target='_blank'>{source_url}</a></p>"

        # Buat objek Artikel
        new_article = Article.objects.create(
            title=title,
            content=final_content,
            author=request.user
        )

        # Proses download gambar (kode ini sudah benar)
        if image_url:
            try:
                img_response = requests.get(image_url, stream=True)
                img_response.raise_for_status()
                file_name = os.path.basename(urlparse(image_url).path)
                new_article.thumbnail.save(
                    file_name,
                    ContentFile(img_response.content),
                    save=True
                )
            except requests.exceptions.RequestException as e:
                print(f"Gagal mengunduh gambar dari {image_url}: {e}")
        
        return redirect('dashboard:manage_articles')
    
    return redirect('dashboard:import_news')

@staff_member_required
def manage_users_view(request):
    # Ambil semua user kecuali superuser
    users = User.objects.filter(is_superuser=False)
    context = {
        'users': users
    }
    return render(request, 'dashboard/manage_users.html', context)

@staff_member_required
def edit_user_view(request, pk):
    """ Halaman untuk mengedit user """
    user_to_edit = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manage_users')
    else:
        form = UserUpdateForm(instance=user_to_edit)
    
    context = {
        'form': form,
        'form_title': f'Edit Pengguna: {user_to_edit.username}'
    }
    return render(request, 'dashboard/user_form.html', context)

@staff_member_required
def delete_user_view(request, pk):
    """ Halaman konfirmasi hapus user """
    user_to_delete = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('dashboard:manage_users')
    
    context = {
        'user_to_delete': user_to_delete
    }
    return render(request, 'dashboard/user_confirm_delete.html', context)