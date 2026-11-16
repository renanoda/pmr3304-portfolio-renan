from html.parser import HTMLParser


class CoverParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.source = ""

    def handle_starttag(self, tag, attrs):
        if tag == "img" and not self.source:
            self.source = dict(attrs).get("src") or ""


from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField("Nome", max_length=100, unique=True)
    description = models.TextField("Descrição")

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"

    def __str__(self):
        return self.name


class Post(models.Model):
    categories = models.ManyToManyField(Category, related_name="posts", verbose_name="Categorias", blank=True)
    title = models.CharField("Título", max_length=200)
    content = models.TextField("Conteúdo em HTML")
    date = models.DateTimeField("Data de publicação", default=timezone.now)

    class Meta:
        ordering = ["-date", "-pk"]

    @property
    def cover_url(self):
        parser = CoverParser()
        parser.feed(self.content)
        return parser.source

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


class PostCover(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="uploaded_cover")
    data = models.BinaryField()
    content_type = models.CharField(max_length=20)
