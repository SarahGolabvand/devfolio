from pathlib import Path
from django.core.files import File
from django.db import transaction
from .models import Project, Screenshot, Tag, Service, StackItem, KeyOutcome

# مسیر دقیق seed_assets نسبت به همین فایل
ASSETS_DIR = Path(__file__).resolve().parent / "seed_assets"

SAMPLE_TAGS = [
    {"name": "API", "display_order": 1},
    {"name": "Website", "display_order": 2},
    {"name": "SaaS", "display_order": 3},
]

SAMPLE_SERVICES = [
    {"title": "REST API Development"},
    {"title": "Database Architecture & Optimization"},
    {"title": "Backend Development"},
]

SAMPLE_PROJECTS = [
    {
        "slug": "open-source-portfolio-website",
        "name": "Open-Source Portfolio Website",
        "short_description": "A modern, Dockerized, dynamic portfolio Website for backend developers powered by Django, Tailwind and Unfold Admin.",
        "article_title": "Building a Self-Hosted, Containerized Portfolio Platform with Django & Unfold",
        "article": (
            "Developed an end-to-end open-source web application designed specifically for backend developers "
            "to showcase their architecture, services, and live projects dynamically. Driven by Django ORM and "
            "containerized via Docker and Poetry, the platform removes the hassle of editing static HTML by providing "
            "a sleek, Tailwind-powered Django Unfold admin panel to manage all portfolio data on the fly.\n\n"
            "Traditional static sites often fail to reflect backend depth or require manual deployments for simple "
            "content updates. This solution bridges that gap with automated database seeding, localized settings, "
            "and full environment isolation—allowing developers to spin up a production-ready showcase in under "
            "two minutes with a single command."
        ),
        "role": "Backend Developer",
        "timeline": "3 Weeks (2026)",
        "demo_url": "https://github.com/",
        "is_published": True,
        "display_order": 1,
        "tags": ["Website"],
        "services": ["Backend Development", "Database Architecture & Optimization"],
        "stack": ["Python", "Django", "Docker", "Tailwind"],
        "outcomes": [
            "Engineered aggregated queries achieving sub-100ms response time.",
            "Configured robust automated testing pipelines.",
            "Designed idempotent background workers for event stream processing.",
        ],
        "screenshots": [
            {
                "file_name": "dark-main.png",
                "alt_text": "Portfolio Dark Theme Main Dashboard",
                "is_primary": True,
            },
            {
                "file_name": "light-main.png",
                "alt_text": "Portfolio Light Theme Overview",
                "is_primary": False,
            },
            {
                "file_name": "panel-admin.png",
                "alt_text": "Django Unfold Modern Admin Panel",
                "is_primary": False,
            },
        ],
    }
]


@transaction.atomic
def seed_projects():
    tags_map = {}
    for tag_data in SAMPLE_TAGS:
        tag_obj, _ = Tag.objects.update_or_create(
            name=tag_data["name"],
            defaults={"display_order": tag_data.get("display_order", 0)},
        )
        tags_map[tag_obj.name] = tag_obj

    services_map = {}
    for service_data in SAMPLE_SERVICES:
        service_obj, _ = Service.objects.update_or_create(
            title=service_data["title"],
        )
        services_map[service_obj.title] = service_obj

    for project_data in SAMPLE_PROJECTS:
        project_fields = {
            "name": project_data["name"],
            "short_description": project_data["short_description"],
            "article_title": project_data["article_title"],
            "article": project_data["article"],
            "role": project_data["role"],
            "timeline": project_data["timeline"],
            "demo_url": project_data.get("demo_url", ""),
            "is_published": project_data.get("is_published", True),
            "display_order": project_data.get("display_order", 0),
        }

        project_obj, _ = Project.objects.update_or_create(
            slug=project_data["slug"],
            defaults=project_fields,
        )

        project_tags = [tags_map[t] for t in project_data.get("tags", []) if t in tags_map]
        project_obj.tags.set(project_tags)

        project_services = [services_map[s] for s in project_data.get("services", []) if s in services_map]
        project_obj.services.set(project_services)

        for stack_name in project_data.get("stack", []):
            StackItem.objects.get_or_create(
                project=project_obj,
                name=stack_name,
            )

        for idx, outcome_text in enumerate(project_data.get("outcomes", []), start=1):
            KeyOutcome.objects.get_or_create(
                project=project_obj,
                key_outcomes=outcome_text,
                defaults={"display_order": idx},
            )

        for idx, shot in enumerate(project_data.get("screenshots", []), start=1):
            file_name = shot["file_name"]
            image_path = ASSETS_DIR / file_name

            screenshot_obj, _ = Screenshot.objects.update_or_create(
                project=project_obj,
                alt_text=shot["alt_text"],
                defaults={
                    "is_primary": shot.get("is_primary", False),
                    "display_order": idx,
                },
            )

            if image_path.exists():
                if not screenshot_obj.image or not screenshot_obj.image.storage.exists(screenshot_obj.image.name):
                    with open(image_path, "rb") as f:
                        screenshot_obj.image.save(file_name, File(f), save=True)
                        print(f"✅ Saved {file_name} for {project_obj.name}")
            else:
                print(f"⚠️ Asset not found: {image_path}")
