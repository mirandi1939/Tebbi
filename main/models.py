from django.db import models

# Create your models here.
from account.models import User


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent.name} --> {self.name}'
        return self.name

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False


class Traning(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    working_time = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tranings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tranings')
    created = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        if self.images.first():
            return self.images.first()
        else:
            return "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'pk': self.pk})


class Image(models.Model):
    image = models.ImageField(upload_to='tranings', default='https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg')
    traning = models.ForeignKey(Traning, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url