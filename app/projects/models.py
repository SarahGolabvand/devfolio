from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Tag(models.Model):
    name = models.CharField(_("tag's name"), max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name


class Project(models.Model):
    tag = models.ForeignKey(
        'Tag',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
    )

    title = models.CharField(_("project's name"), max_length=100)
    slug = models.SlugField(_('slug'), max_length=255, unique=True, blank=True)
    description = models.CharField(_("description"), max_length=250)

    overview_title = models.CharField(_("article_title"), max_length=250)

    role = models.CharField(_("Role"), max_length=50)
    timeline = models.CharField(_("timeline"), max_length=50)

    demo_url = models.URLField(_("demo url"), blank=True)

    # screenshots -> FK
    # key_outcomes -> FK
    # stack_items -> FK
    # overview_paragraphs -> FK

    is_published = models.BooleanField(_(" is published"), default=False)
    display_order = models.PositiveIntegerField(_("display order"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectOverviewParagraph(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='overview_paragraphs')
    text = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f'{self.project.title} paragraph {self.display_order}'


class ProjectScreenshots(models.Model):
    project = models.ForeignKey("Project", verbose_name=_(
        "project"), on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(_("screenshot"), upload_to='projects/screenshots/',
                              height_field=None, width_field=None, max_length=None)
    alt_text = models.CharField(_("alt text"), max_length=250, blank=True)

    is_primary = models.BooleanField(_("is primary"))
    display_order = models.PositiveIntegerField(_("display order"), default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f'{self.project.title} screenshot'


class ProjectKeyOutcome(models.Model):

    project = models.ForeignKey("Project", verbose_name=_(
        "project's tags"), on_delete=models.CASCADE, related_name='key_outcomes')

    key_outcomes = models.CharField(_("key_outcomes"), max_length=250)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name


class ProjectStackItem(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='stack_items')
    name = models.CharField(max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name
