from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from students.models import CustomUser
# from django.utils.translation import gettext_lazy as _
class Subject(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering=['title']
    def __str__(self):
        return self.title

class Course(models.Model):
    owner=models.ForeignKey(CustomUser, related_name='courses_created', on_delete=models.CASCADE, verbose_name='Владелец')
    subject=models.ForeignKey(Subject,related_name='courses', on_delete=models.CASCADE, verbose_name='Предмет')
    title=models.CharField(verbose_name='Название',max_length=200)
    slug=models.SlugField(verbose_name='slug',max_length=200, unique=True)
    overview=models.TextField(verbose_name='Описание')
    created=models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(CustomUser,related_name='courses_joined',blank=True)
    # my
    applications = models.ManyToManyField(CustomUser,related_name='courses_applied',blank=True)
    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.title
    
class Module(models.Model):
    course=models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title=models.CharField(verbose_name='Название',max_length=200)
    description=models.TextField(verbose_name='Описание',blank=True)
    order=OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}.{self.title}'
    
    class Meta:
        ordering=['order']
    
class Content(models.Model):
    module=models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('text', 'video', 'image', 'file')})
    object_id=models.PositiveIntegerField()
    item=GenericForeignKey('content_type', 'object_id')
    order=OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering=['order']
        
class ItemBase(models.Model):
    owner=models.ForeignKey(CustomUser, related_name='%(class)s_related', on_delete=models.CASCADE)
    title=models.CharField(verbose_name='Название',max_length=250)
    creted=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

    def __str__(self):
        return self.title
    
    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item':self})
    
class Text(ItemBase):
    content=models.TextField()

class File(ItemBase):
    file=models.FileField(verbose_name='Файл',upload_to='files')

class Image(ItemBase):
    file=models.FileField(verbose_name='Изображение',upload_to='images')

class Video(ItemBase):
    url=models.URLField()

    def slasher(self):
        return str(self.url).split('/')[-2]