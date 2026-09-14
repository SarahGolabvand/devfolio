import os
from django.core.management.base import BaseCommand
from accounts.services import seed_accounts
from projects.services import seed_projects


class Command(BaseCommand):
    help = "Seeds the database with initial portfolio data using .env credentials"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL("Starting database seeding..."))

        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not email or not password:
            self.stderr.write(
                self.style.ERROR(
                    "❌ ADMIN_EMAIL or ADMIN_PASSWORD not found in environment variables!"
                )
            )
            return

        self.stdout.write(self.style.WARNING(f"\n--- Seeding Account ({email}) ---"))
        try:
            seed_accounts(email, password)
            self.stdout.write(self.style.SUCCESS("✓ Accounts seeded successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to seed accounts: {e}"))
            return

        self.stdout.write(self.style.MIGRATE_LABEL("\n--- Seeding Projects ---"))
        try:
            seed_projects()
            self.stdout.write(self.style.SUCCESS("✓ Projects & assets seeded successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Failed to seed projects: {e}"))
            return

        self.stdout.write(self.style.SUCCESS("\n🎉 All tasks completed!"))
