from random import randint

from django.db import models

from category.models import Category


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=5000, blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts',
                                 on_delete=models.SET_NULL, null=True)
    preview = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} - {self.title[:25]}'

    class Meta:
        ordering = ('created_at',)

class PostImage(models.Model):
    title = models.CharField(max_length=100,
                             blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, related_name='images',
                             on_delete=models.CASCADE)

    def generate_name(self):
        return 'image' + str(randint(100000, 999999))
    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImage, self).save(*args, **kwargs)