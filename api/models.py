from django.db import models

# Create your models here.


class NewsPost(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(null=True, blank=True)
    article_id = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class CommentPost(models.Model):
    post_id = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self) -> str:
        return self.author
