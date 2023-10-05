from django.core.management.base import BaseCommand
from core.models import Profile, Pairing


class Command(BaseCommand):
    help = "Sets all users to deactivated - useful for end of a semester"

    # define logic of command
    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            profile.active = False
            profile.crush = None
            profile.has_tag_pairing = False
            profile.tag_pairing = None
            profile.tag_pairing2 = None

            profile.save()
        
        Pairing.objects.all().delete()