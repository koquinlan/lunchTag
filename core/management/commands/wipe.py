from django.core.management.base import BaseCommand
from core.models import Edge, Profile, Pairing
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Wipes all user preferences, profiles and pairings. Designed for use after a run of lunch tags"

    # define logic of command
    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            profile.image = None
            profile.active = True
            profile.pronouns = 'pronouns'
            profile.phone = '(xxx) xxx-xxxx'
            profile.strikes.through.objects.all().delete()
            profile.crush = None
            profile.has_tag_pairing = False
            profile.tag_pairing = None
            profile.tag_pairing2 = None

            profile.save()
        
        for edge in Edge.objects.all():
            edge.active = True
            edge.weight = 100.0
        
        Pairing.objects.all().delete()