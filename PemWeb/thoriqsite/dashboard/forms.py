from django.contrib.auth.models import User 
from django import forms
from articles.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'thumbnail'] # Tentukan field yang ingin ditampilkan di form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Tentukan field mana yang bisa diubah oleh admin
        fields = ['username', 'email', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }