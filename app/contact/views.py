from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.shortcuts import redirect
# Create your views here.

from django.views.generic import CreateView

from .forms import ContactForm
from .models import ContactMessage


class ContactSubmitView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def form_valid(self, form):
        """send email to admin then save message in db"""

        # send email to admin
        data = form.cleaned_data
        self.send_admin_email(data)

        # send message to telegram bot
        # self.send_to_telegram(data)

        # show messages logs
        messages.success(self.request, 'your message sended successful')

        # save message in db
        self.object = form.save()

        # redirect client in before path who was in
        return redirect(self.request.META.get("HTTP_REFERER", "/"))

    def form_invalid(self, form):
        """
        show error log for devloper and an error message for client 
        """
        
        print(form.errors, flush=True)
        return redirect(self.request.META.get("HTTP_REFERER", "/"))

    def send_admin_email(self, data):
        subject = f"New website message: {data['subject']}"
        message = f"from: {data['name']} ({data['email']})\n\nMessage:\n{data['message']}"

        send_mail(subject, message,
                  None,
                  ['glbvnd@gmail.com'],
                  fail_silently=False)

    def send_to_telegram(self, data):
        # اینجا بعداً کد ربات تلگرامت رو می‌نویسی
        pass
