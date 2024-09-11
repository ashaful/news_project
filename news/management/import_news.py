# news/management/commands/import_news.py

import csv
from django.core.management.base import BaseCommand
from news.models import NewsArticle

class Command(BaseCommand):
    help = 'Import news articles from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                NewsArticle.objects.update_or_create(
                    title=row['title'],
                    defaults={
                        'link': row['link'],
                        'newspaper': row['newspaper'],
                        'date': row['date'],
                        'time': row['time'],
                        'category': row['category']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported news articles'))
