# articles/models.py
from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True}
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        null=True, 
        blank=True, 
        help_text="Gambar thumbnail untuk artikel"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']