# users/views.py
from django.shortcuts import redirect, render # tambahkan render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from articles.models import Article # Kita akan butuh ini untuk menampilkan artikel user

def home_dispatch_view(request):
    """
    Mengarahkan pengguna berdasarkan perannya setelah login.
    - Admin/Staff ke dashboard.
    - User biasa atau Guest ke halaman daftar artikel.
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect(reverse('dashboard:index')) # Arahkan admin ke dashboard
    
    # Untuk user biasa yang terotentikasi atau session guest
    if request.user.is_authenticated or request.session.get('is_guest'):
        return redirect(reverse('articles:list')) # Arahkan user/guest ke daftar artikel
    
    # Jika tidak ada sesi sama sekali (seharusnya tidak terjadi, tapi untuk jaga-jaga)
    return redirect(reverse('pages:welcome'))

# ... (sisa view guest_login_view Anda) ...
def guest_login_view(request):
    request.session['is_guest'] = True
    # Arahkan ke dispatch view setelah login sebagai guest
    return redirect(reverse('users:home_dispatch'))

@login_required
def profile_view(request):
    # Mengambil artikel yang ditulis oleh user yang sedang login (jika dia staff)
    user_articles = Article.objects.filter(author=request.user)

    if request.method == 'POST':
        # Proses form jika ada data yang dikirim
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Arahkan kembali ke halaman profil dengan pesan sukses (opsional)
            return redirect('users:profile') 
    else:
        # Tampilkan form dengan data user saat ini
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'articles': user_articles
    }
    return render(request, 'users/profile.html', context)