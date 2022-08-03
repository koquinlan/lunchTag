from django.core.management.base import BaseCommand
from core.models import Edge
from core.utils import make_pairings, push_pairings


class Command(BaseCommand):
    help = "Creates and pushes the pairings to everyone"

    # define logic of command
    def handle(self, *args, **options):
        push_pairings(make_pairings())