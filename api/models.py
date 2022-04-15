from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
# C:/Users/Lenovo/Envs/web/Scripts/activate.bat


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.title), filename])


SOTRIE_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
)


class Category(MPTTModel):

    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True)
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ((
            'parent',
            'slug',
        ))
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]

        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs

    def __str__(self):
        return self.name


class Article(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = TreeForeignKey('Category',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    image = models.ImageField(
        upload_to=nameFile, max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    storie = RichTextField(blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    storie_positions = models.CharField(
        max_length=20, choices=SOTRIE_CHOICES, null=True, default=None, blank=True)
    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    # def __str__(self):
    #     return self.title
