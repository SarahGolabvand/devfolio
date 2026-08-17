from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email'),)
    subject = models.CharField(_('subject'),max_length=200)
    message = models.TextField(_('message'),)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"

