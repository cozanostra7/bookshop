from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255,verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category',kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class  Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок статьи')
    description = models.TextField(default='Здесь будет текст',verbose_name="Описание")
    image = models.ImageField(upload_to='images/',blank=True,null=True,verbose_name="Изображение")
    views = models.PositiveIntegerField(default=0,verbose_name="Просмотры")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Дата обновления")

    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles',blank=True,null=True)
    bio = models.CharField(max_length = 255,verbose_name= 'Bio',blank=True,null=True)
    birth_date= models.DateTimeField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse('profile',kwargs={'pk':self.user.pk})

    def get_profile_image(self):
        if self.profile_image:
            try:
                return self.profile_image.url
            except:
                return 'https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg'
        else:
            return 'https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg'

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


