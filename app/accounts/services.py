from django.contrib.auth import get_user_model
from .models import ProfileModel, SkillsModel

User = get_user_model()


def seed_accounts(input_email, input_password) -> User:
    email = input_email
    password = input_password


    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )


    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()

    if created:
        print(f"✅ Superuser {email} created. password : {password}")
    else:
        print(f"✅ Superuser {email} refreshed. password : {password}")


    profile, _ = ProfileModel.objects.update_or_create(
        user=user,
        defaults={
            "first_name": "Admin",
            "last_name": "User",
            "location": "Earth",
            "bio": """
        Dedicated Backend Developer specializing in Python and Django architectures.
        Focused on building robust, scalable RESTful APIs, containerized environments, and clean database designs.""",
            "email": "robert@example.com",
            "phone_number": "+100003823332",
            "github": "https://github.com",
            "linkedin": "https://linkedin.com/",
            "telegram": "https://t.me/",
        },
    )
    print("✅ Profile synced.")


    initial_skills = [
        {"abbreviation": "PY", "title": "Python",
            "description": "Backend Development", "color_theme": "blue", "order": 1},
        {"abbreviation": "DJ", "title": "Django",
            "description": "Web Framework", "color_theme": "emerald", "order": 2},
        {"abbreviation": "DK", "title": "Docker",
            "description": "Containerization", "color_theme": "orange", "order": 3},
    ]

    for skill_data in initial_skills:
        SkillsModel.objects.update_or_create(
            title=skill_data["title"],
            defaults=skill_data,
        )
    print("✅ Skills seeded.")

    return user
