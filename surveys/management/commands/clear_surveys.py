from django.core.management import BaseCommand
from django.utils import timezone

from surveys.models import *


class Command(BaseCommand):
    help = "Clear Surveys - Delete Sources."

    def handle(self, *args, **options):
        start_time = timezone.now()

        print('Delete sources')
        sources = eROSITA.objects.all()
        sources.delete()

        print('Delete meta objects')
        meta_objects = MetaObject.objects.all()
        meta_objects.delete()

        print('Delete meta groups')
        meta_objects = MetaGroup.objects.all()
        meta_objects.delete()

        print('Delete origin files')
        meta_sources = OriginFile.objects.all()
        meta_sources.delete()

        self.stdout.write(f'End clearing surveys')
        end_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(f'Clearing took: {(end_time-start_time).total_seconds()} seconds.'))
