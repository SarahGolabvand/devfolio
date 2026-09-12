# core/management/command/seed_data.py

import getpass
from django.core.management.base import BaseCommand
from accounts.services import seed_accounts
from projects.services import seed_projects


class Command(BaseCommand):
    help = "Seeds the database with initial portfolio data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL(
            "Starting database seeding..."))

        self.stdout.write(self.style.WARNING("\n--- Account Setup ---"))
        email = input("Enter Admin Email: ").strip()
        password = getpass.getpass("Enter Admin Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")

        if password != confirm_password:
            self.stderr.write(self.style.ERROR(
                "❌ Passwords do not match! Aborting."))
            return

        try:
            seed_accounts(email, password)
            self.stdout.write(self.style.SUCCESS(
                "✓ Accounts seeded successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"❌ Failed to seed accounts: {e}"))
            return

        self.stdout.write(self.style.MIGRATE_LABEL(
            "\n--- Seeding Projects ---"))
        try:
            seed_projects()
            self.stdout.write(self.style.SUCCESS(
                "✓ Projects & assets seeded successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"❌ Failed to seed projects: {e}"))

        self.stdout.write(self.style.SUCCESS("\n🎉 All tasks completed!"))
