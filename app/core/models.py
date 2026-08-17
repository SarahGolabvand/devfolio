from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        AbstractUser, BaseUserManager)

from django.conf import settings
# Create your models here.

# Authentication and Authorization


class UserManager(BaseUserManager):
    """
    Custom User Model Manager where email is the unique identifiers for Authentication instead of username or extra data
    """

    def create_user(self, email, password, **extra_fields):
        """
        create and save a User with the given email and password"""
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """create and save a SuperUser with the given email and password or extra data"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff True"))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser True"))

        return self.create_user(email, password, **extra_fields)

    def __str__(self):
        return super().__str__()


class User(AbstractBaseUser, PermissionsMixin):
    """
    It's the global custom user model
    """
    class Meta:
        db_table = 'accounts_users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    email = models.EmailField(_("Email"), max_length=254, unique=True)
    is_staff = models.BooleanField(
        _("is staff"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)
    is_superuser = models.BooleanField(
        _("is superuser"), default=False)
    # is_verified=models.BooleanField(_("کاربر تايید شده؟"),default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    created_at = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.email

# About section


class ProfileModel(models.Model):
    """ Handle About
    """
    class Meta:
        db_table = 'accounts_profiles'
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "user"), on_delete=models.CASCADE)
    first_name = models.CharField(
        _("first_name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(
        _("last name"), max_length=50, blank=True, null=True)
    avatar = models.ImageField(
        _("Avatar"), blank=True, null=True, upload_to='avatars/', help_text='Recommended: 1200 × 1500 px')

    text_banner = models.CharField(_("Text Banner"), max_length=50)
    bio = models.TextField(
        _("biography"), max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(
        _("updated at"), auto_now=True, auto_now_add=False)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_email(self):
        return self.user.email

    def __str__(self):
        return self.get_email()


class SkillsModel(models.Model):

    class Meta:
        db_table = 'accounts_skills'
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ['order', 'title']

    COLOR_THEMES = [
        ('emerald', 'سبز زمردی'),
        ('blue', 'آبی آسمانی'),
        ('orange', 'نارنجی'),
        ('purple', 'بنفش'),
        ('red', 'قرمز'),
        ('slate', 'خاکستری'),
    ]

    abbreviation = models.CharField(
        max_length=5, help_text="like `DJ `for django ")

    color_theme = models.CharField(
        max_length=20,
        choices=COLOR_THEMES,
        default='emerald'
    )

    title = models.CharField(_("skill title"), max_length=25)
    description = models.CharField(_("description"), max_length=80)
    order = models.PositiveIntegerField(
        default=0, help_text="display ordering")
    is_visible = models.BooleanField(default=True)

    @property
    def get_color_classes(self):

        mapping = {

            'emerald': 'grid size-11 place-items-center rounded-xl bg-emerald-500/10 text-sm font-black text-emerald-700 dark:text-emerald-400',

            'blue': 'grid size-11 place-items-center rounded-xl bg-blue-500/10 text-sm font-black text-blue-700 dark:text-blue-400',
            'orange': 'grid size-11 place-items-center rounded-xl bg-orange-500/10 text-sm font-black text-orange-700 dark:text-orange-400',
            'purple': 'grid size-11 place-items-center rounded-xl bg-purple-500/10 text-sm font-black text-purple-700 dark:text-purple-400',
            'red': 'grid size-11 place-items-center rounded-xl bg-red-500/10 text-sm font-black text-red-700 dark:text-red-400',
            'slate': 'grid size-11 place-items-center rounded-xl bg-slate-500/10 text-sm font-black text-slate-700 dark:text-slate-400',
        }
        return mapping.get(self.color_theme, mapping['emerald'])

    def __str__(self):
        return self.title
