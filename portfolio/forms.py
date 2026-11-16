from html.parser import HTMLParser

from django import forms
from django.db import transaction
from django.urls import reverse
from django.utils.html import format_html, linebreaks

from .models import Comment, Post, PostCover


class ProjectBody(HTMLParser):
    """Recover editable paragraphs and the existing cover from stored HTML."""

    def __init__(self, content):
        super().__init__()
        self.parts = []
        self.cover_tag = ""
        self.feed(content)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "img" and not self.cover_tag:
            self.cover_tag = self.get_starttag_text()
        elif tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"p", "div", "li", "h2", "h3"}:
            self.parts.append("\n\n")

    def handle_data(self, data):
        self.parts.append(data)

    @property
    def text(self):
        return "".join(self.parts).strip()


class PostForm(forms.ModelForm):
    text = forms.CharField(label="Texto", widget=forms.Textarea(attrs={"rows": 10}))
    cover = forms.FileField(
        label="Imagem de capa", required=False,
        help_text="Escolha uma foto JPG, PNG ou WebP de até 5 MB.",
        widget=forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
    )

    class Meta:
        model = Post
        fields = ["title", "text", "cover", "categories"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = ProjectBody(self.instance.content)
        self.initial["text"] = self.body.text

    def clean_cover(self):
        upload = self.cleaned_data["cover"]
        if not upload:
            return None
        if upload.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Escolha uma imagem de até 5 MB.")
        header = upload.read(32)
        upload.seek(0)
        if header.startswith(b"\xff\xd8\xff"):
            mime = "image/jpeg"
        elif header.startswith(b"\x89PNG\r\n\x1a\n") and header[12:16] == b"IHDR":
            mime = "image/png"
        elif header.startswith(b"RIFF") and header[8:12] == b"WEBP":
            mime = "image/webp"
        else:
            raise forms.ValidationError("Selecione um arquivo JPG, PNG ou WebP.")
        upload.content_type = mime
        return upload

    @transaction.atomic
    def save(self):
        post = super().save(commit=False)
        upload = self.cleaned_data["cover"]
        text = self.cleaned_data["text"]
        if upload or text != self.body.text or not post.pk:
            paragraphs = linebreaks(text, autoescape=True)
            post.content = self.body.cover_tag + paragraphs
        post.save()
        if upload:
            PostCover.objects.update_or_create(
                post=post, defaults={"data": upload.read(), "content_type": upload.content_type}
            )
            src = reverse("post_cover", args=[post.pk])
            post.content = str(format_html('<img class="post-cover" src="{}" alt="">', src)) + paragraphs
            post.save(update_fields=["content"])
        self.save_m2m()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
