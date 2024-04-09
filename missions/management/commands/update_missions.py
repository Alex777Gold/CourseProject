from django.core.management.base import BaseCommand
from missions.api import update_missions


class Command(BaseCommand):
    help = 'Updates missions in the database'

    def handle(self, *args, **options):
        update_missions()
        self.stdout.write(self.style.SUCCESS('Missions updated successfully'))
