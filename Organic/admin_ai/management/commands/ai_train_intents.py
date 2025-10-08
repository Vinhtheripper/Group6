from django.core.management.base import BaseCommand
from admin_ai.core_ai.intent_trainer import train_and_save

class Command(BaseCommand):
    help = "Train intent classifier (TF-IDF + LogisticRegression)"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Training intent classifier...")
        train_and_save()
        self.stdout.write(self.style.SUCCESS("✅ Done."))
