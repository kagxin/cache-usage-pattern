from django.db import models
# from contextlib import
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField(blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'


class Comment(models.Model):
    text = models.TextField(blank=False)
    article = models.ForeignKey(Article, blank=False, related_name='comments')

    def __str__(self):
        return self.text[:10]
    
    class Meta:
        db_table = 'comment'

