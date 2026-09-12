from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .models import ProfileModel, SkillsModel

User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user_successful(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="StrongPassword123!"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("StrongPassword123!"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password123")

    def test_create_superuser_successful(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="AdminPassword123!"
        )
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_create_superuser_invalid_flags_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin2@example.com",
                password="password123",
                is_staff=False
            )


class ProfileModelTests(TestCase):
    def setUp(self):
        # با ساخت یوزر، سیگنال post_save خودبه‌خود پروفایل رو می‌سازه
        self.user = User.objects.create_user(
            email="admin@example.com",
            password="password123"
        )
        # به جای create مجدد، پروفایل ساخته‌شده توسط سیگنال رو واکشی و فیلدهاش رو پر می‌کنیم
        self.profile = ProfileModel.objects.get(user=self.user)
        self.profile.first_name = "Admin"
        self.profile.last_name = "User"
        self.profile.location = "Tehran"
        self.profile.github = "https://github.com/admin"
        self.profile.save()

    def test_fullname_property(self):
        self.assertEqual(self.profile.fullname, "Admin User")

    def test_default_avatar_url_when_none(self):
        self.assertIn("default-avatar.png", self.profile.avatar_url)

    def test_links_property_structure(self):
        links = self.profile.links
        self.assertEqual(links["github"], "https://github.com/admin")
        self.assertEqual(links["telegram"], "")


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="admin@example.com",
            password="password123"
        )

        SkillsModel.objects.create(
            title="Django",
            abbreviation="DJ",
            description="Backend framework",
            is_visible=True,
            order=1
        )
        SkillsModel.objects.create(
            title="Hidden Skill",
            abbreviation="HS",
            description="Should not appear",
            is_visible=False,
            order=2
        )

    def test_index_page_status_code_and_context(self):
        # بررسی روت اصلی با استفاده از مسیر مستقیم '/' یا reverse
        try:
            url = reverse("accounts:index")
        except Exception:
            try:
                url = reverse("index")
            except Exception:
                url = "/"  # فال‌بک مستقیم به روت اصلی پورتفولیو
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index/index.html")
        
        skills = response.context["skills"]
        self.assertEqual(len(skills), 1)
        self.assertEqual(skills[0].title, "Django")
