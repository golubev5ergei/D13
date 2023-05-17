from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', null=True)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    body = models.TextField()
    image = models.ImageField(null=True, blank=True)
    video = models.FileField(upload_to='video/', null=True, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

        
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


CATEGORIES = (
    ('Tanks', 'Танки'),
    ('Hill', 'Хилы'),
    ('DD', 'ДД'),
    ('Merchants', 'Торговцы'),
    ('Guildmaster', 'Гилдмастеры'),
    ('Questgivers', 'Квестгиверы'),
    ('Blacksmith', 'Кузнецы'),
    ('Leatherman', 'Кожевники'),
    ('Potionist', 'Зельевары'),
    ('SpellMaster', 'Мастера заклинаний'),

)


class Category(models.Model):
    name = models.CharField(max_length=250, choices=CATEGORIES, blank=False, default=None)

    def __str__(self):
        return dict(CATEGORIES)[self.name]
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_img')

    def __str__(self):
        return f'{self.user.username} Profile'