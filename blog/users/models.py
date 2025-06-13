from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
import os
from django.utils.text import slugify



from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import re

def slugify_cyrillic(value):
    """
    Транслитерация + slugify: 'Иван Иванов' -> 'ivan-ivanov'
    """
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo','ж': 'zh','з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts','ч': 'ch',
        'ш': 'sh','щ': 'sch','ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu','я': 'ya'
    }
    value = value.lower()
    value = ''.join(translit_dict.get(char, char) for char in value)
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return slugify(value)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="img/", default='img/sbcf-default-avatar.png',blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.pk is None:
            base = self.user.get_full_name() or self.user.username
            base_slug = slugify_cyrillic(base)
            slug = base_slug
            counter = 1
            while Profile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

