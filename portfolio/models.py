from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField("Título", max_length=200)
    content = models.TextField("Conteúdo em HTML")
    date = models.DateTimeField("Data de publicação", default=timezone.now)

    class Meta:
        ordering = ["-date", "-pk"]

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Comentário")
    date = models.DateTimeField("Data de postagem", default=timezone.now)

    class Meta:
        ordering = ["-date", "-pk"]

    def __str__(self):
        return f"{self.author} — {self.post}"

