from django.db import models
from django.urls import reverse


class Article(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=100)

    def __str__(self):
        return "{}-{}-{}".format(self.id, self.author, self.title)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs=dict(id=self.id))
