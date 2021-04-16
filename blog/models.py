from bs4 import BeautifulSoup
from ckeditor_uploader.fields import RichTextUploadingField

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from .utils import is_ru


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True, unique=True,
                             verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             default=None, verbose_name='Автор')
    body = RichTextUploadingField(verbose_name='Пост')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts',
                                  verbose_name='Тэг')
    date_pub = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    image_preview = models.ImageField(upload_to='images/', verbose_name='Изображение',
                                      null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        title_split = self.title.split()
        if len(title_split) > 3:
            title = ' '.join(title_split[:3])
            self.slug = is_ru(title)
        else:
            self.slug = is_ru(self.title)
        super().save(*args, **kwargs)

    def get_preview_post(self):
        """Get a preview of the post."""
        soup = BeautifulSoup(self.body, features='html.parser')
        post = soup.get_text().strip().split('\n')
        if len(post) > 2:
            preview = '<br>'.join(post[:2])
        else:
            preview = '<br>'.join(post)
        return preview

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True,
                             verbose_name='Наименование')
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.slug = is_ru(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    body = models.TextField(u'Комментарий')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    def get_post_url(self):
        """Get the url of the post to which this comment belongs."""
        return reverse('post_detail_url', kwargs={'slug': self.post.slug})


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)
