from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import re
from users.models import Profile
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


from django.contrib.auth.models import User

def slugify_cyrillic(value):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    value = value.lower()
    value = ''.join(translit_dict.get(c, c) for c in value)
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return slugify(value)


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')


class Plant(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=400)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    image=models.ImageField(upload_to='img/',default='img/noimage.jpg',blank=True)
    slug=models.SlugField(unique=True,blank=True)
    category=models.ForeignKey('Category',on_delete=models.PROTECT)
    #author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    tag= models.ManyToManyField('Tag', blank=True)
    author= models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    votes = GenericRelation(LikeDislike)
    @property
    def likes(self):
        return self.votes.filter(vote=1).count()
    @property
    def dislikes(self):
        return self.votes.filter(vote=-1).count()
        
    @property
    def get_content_type_id(self):
        return ContentType.objects.get_for_model(self.__class__).id

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Plant.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('plant', kwargs={'slug': self.slug})



class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField( unique=True, db_index=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField( unique=True, db_index=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



class Comment(models.Model):
    comment=models.TextField(max_length=200)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    post = models.ForeignKey(  
        Plant,  
        on_delete=models.CASCADE,  
        verbose_name="Пост",  
        related_name="comments",  
    )


    def __str__(self):  
        return f"Комментарий от {self.author} к посту {self.post}"
    


