from django.test import TestCase, Client
from django.urls import reverse
from .models import Project, Tag, Screenshot, StackItem, Service


class ProjectModelTests(TestCase):
    def test_slug_auto_generated_on_save(self):
        project = Project.objects.create(
            name="Scalable Microservice Architecture",
            short_description="High-throughput payment gateway",
            article_title="Building the Gateway",
            article="Paragraph 1\n\nParagraph 2",
            role="Backend Lead",
            timeline="6 months",
            is_published=True
        )
        self.assertEqual(project.slug, "scalable-microservice-architecture")
        self.assertEqual(str(project), "Scalable Microservice Architecture")

    def test_project_relations(self):
        project = Project.objects.create(
            name="Django Portfolio",
            short_description="Developer portfolio site",
            article_title="Overview",
            article="Full text here",
            role="Developer",
            timeline="1 month"
        )
        tag = Tag.objects.create(name="Django", display_order=1)
        service = Service.objects.create(title="Backend Development")
        project.tags.add(tag)
        project.services.add(service)

        StackItem.objects.create(
            project=project, name="Docker", display_order=1)
        Screenshot.objects.create(
            project=project, alt_text="Home screen", is_primary=True)

        self.assertEqual(project.tags.count(), 1)
        self.assertEqual(project.services.count(), 1)
        self.assertEqual(project.stack_items.count(), 1)
        self.assertEqual(project.screenshots.count(), 1)
        self.assertEqual(str(tag), "Django")
        self.assertEqual(str(service), "Backend Development")


class ProjectViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.published_project = Project.objects.create(
            name="Public API",
            short_description="An open API project",
            article_title="Public Docs",
            article="Some content",
            role="Architect",
            timeline="3 months",
            is_published=True
        )
        self.draft_project = Project.objects.create(
            name="Confidential Project",
            short_description="Secret project under NDA",
            article_title="Secret Docs",
            article="Hidden content",
            role="Consultant",
            timeline="Ongoing",
            is_published=False
        )

    def test_project_list_view_filters_only_published(self):
        try:
            url = reverse("projects:projects_list")
        except Exception:
            try:
                url = reverse("projects_list")
            except Exception:
                url = "/projects/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # لیست پروژه‌ها نباید شامل پروژه‌های پیش‌نویس باشد
        projects_in_context = response.context["projects"]
        self.assertIn(self.published_project, projects_in_context)
        self.assertNotIn(self.draft_project, projects_in_context)

    def test_project_detail_view_success(self):
        try:
            url = reverse("projects:project_detail", kwargs={
                          "slug": self.published_project.slug})
        except Exception:
            try:
                url = reverse("project_detail", kwargs={
                              "slug": self.published_project.slug})
            except Exception:
                url = f"/projects/{self.published_project.slug}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["project_obj"], self.published_project)

    def test_project_detail_view_not_found(self):
        try:
            url = reverse("projects:project_detail", kwargs={
                          "slug": "non-existent-project"})
        except Exception:
            try:
                url = reverse("project_detail", kwargs={
                              "slug": "non-existent-project"})
            except Exception:
                url = "/projects/non-existent-project/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
