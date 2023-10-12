from django.core.management.base import BaseCommand
from core.models import Profile


class Command(BaseCommand):
    help = "Counts the number of active users"

    # define logic of command
    def handle(self, *args, **options):
        numActive = 0

        for profile in Profile.objects.all():
            if profile.active == False:
                numActive += 1

        print("Number of active users: " + str(numActive))
