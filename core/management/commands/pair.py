from django.core.management.base import BaseCommand
from core.models import Edge
from core.utils import make_pairings


class Command(BaseCommand):
    help = "Scrape the past day for articles"

    # define logic of command
    def handle(self, *args, **options):
        make_pairings()