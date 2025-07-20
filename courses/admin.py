from django.contrib import admin
from .models import Subject, Course, Module, Content
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Course, Module, Content, Text, Video, Image, File
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=['title', 'slug']
    prepopulated_fields={'slug':('title',)}

# class ModuleInline(admin.StackedInline):
#     model=Module

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display=['title', 'subject', 'created']
#     list_filter=['created', 'subject']
#     search_fields=['title', 'overview']
#     prepopulated_fields={'slug':('title',)}
#     inlines=[ModuleInline]
#     filter_horizontal = ('students','applications') # добавление студентов

class TextInline(admin.StackedInline):
    model = Text

class VideoInline(admin.StackedInline):
    model = Video

class ImageInline(admin.StackedInline):
    model = Image

class FileInline(admin.StackedInline):
    model = File

# GenericInline для Content
class ContentInline(GenericTabularInline):
    model = Content
    extra = 1
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    classes = ['collapse']
    def item_preview(self, instance):
        if instance.item:
            return str(instance.item)
        return "-"
    item_preview.short_description = "Просмотр контента"
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['module', 'content_type', 'object_id', 'item', 'order']
    list_filter = ['module__course', 'content_type']
    search_fields = ['module__title']
    
    def item(self, obj):
        return str(obj.item)
    item.short_description = 'Контент'
# Inline для Module
class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    show_change_link = True
    inlines = [ContentInline]  # Добавляем вложенные GenericInlines

# Админка для Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'owner']
    list_filter = ['subject', 'created']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]  # Добавляем ModuleInline
    
    # Для удобного управления студентами и заявками
    filter_horizontal = ['students', 'applications']

# Админка для Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'description']
    inlines = [ContentInline]  # Добавляем ContentInline

# Регистрация моделей контента
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']
    
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']