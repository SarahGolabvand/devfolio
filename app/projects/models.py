from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Project(models.Model):

    slug = models.SlugField(_('slug'), max_length=255, unique=True, blank=True)
    thumbnail = models.ImageField(_("thumbnail"),
                                  upload_to='project/thumbnails', null=True, blank=True)
    name = models.CharField(_("project's name"), max_length=100)
    short_description = models.CharField(_("short description"),
                                         max_length=250)
    article_title = models.CharField(_("Article Title"), max_length=250)
    article = models.TextField(
        _("Article"), help_text='split paragraphs with an Enter')
    role = models.CharField(_("Role"), max_length=50)
    timeline = models.CharField(_("timeline"), max_length=50)
    demo_url = models.URLField(_("demo url"), blank=True)
    is_published = models.BooleanField(_(" is published"), default=False)
    display_order = models.PositiveIntegerField(_("display order"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        db_table = 'projects'

    @property
    def paragraphs(self):
        return self.article.split("\n\n")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Screenshots(models.Model):
    class Meta:
        ordering = ['display_order', 'id']
        db_table = 'projects_screenshots'

    project = models.ForeignKey("Project", verbose_name=_(
        "project"), on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(_("screenshot"), upload_to='projects/screenshots/',
                              height_field=None, width_field=None, max_length=None)
    alt_text = models.CharField(_("alt text"), max_length=250, blank=True)

    is_primary = models.BooleanField(_("is primary"))
    display_order = models.PositiveIntegerField(_("display order"), default=0)

    def __str__(self):
        return f'{self.alt_text} screenshot'


class KeyOutcome(models.Model):
    class Meta:
        ordering = ['display_order', 'id']
        db_table = 'projects_key_outcomes'

    project = models.ForeignKey("Project", verbose_name=_(
        "project's tags"), on_delete=models.CASCADE, related_name='key_outcomes')

    key_outcomes = models.CharField(_("key_outcomes"), max_length=250)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.key_outcomes


class StackItem(models.Model):
    class Meta:
        ordering = ['display_order', 'id']
        db_table = 'project_stack_items'

    project = models.ForeignKey("Project", verbose_name=_(
        "project's stacks"), on_delete=models.CASCADE, related_name='stack_items')
    name = models.CharField(max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Tag(models.Model):

    project = models.ForeignKey(
        'Project', related_name='tags', on_delete=models.CASCADE)
    name = models.CharField(_("tag's name"), max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name


class Services(models.Model):
    class Meta:
        db_table = 'projects_services'

    project = models.ForeignKey("Project", verbose_name=_("project's services"), on_delete=models.CASCADE,
                                related_name='services')
    title = models.CharField(_("title"), max_length=70)

    def __str__(self):
        return self.title
