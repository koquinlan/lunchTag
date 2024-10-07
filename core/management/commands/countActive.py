from django.core.management.base import BaseCommand
from core.models import Profile


class Command(BaseCommand):
    help = "Counts the number of active users"

    # define logic of command
    def handle(self, *args, **options):
        tot = 0
        numActive = 0

        for profile in Profile.objects.all():
            tot += 1
            if profile.active == True:
                numActive += 1

        print("Number of active users: " + str(numActive))
        print("Total users: " + str(tot))
