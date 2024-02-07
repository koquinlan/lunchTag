# file: yourapp/management/commands/merge_accounts.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Edge

class Command(BaseCommand):
    help = 'Merge two user accounts by transferring associated data'

    def add_arguments(self, parser):
        parser.add_argument('old_username', type=str, help='Username of the old account')
        parser.add_argument('new_username', type=str, help='Username of the new account')

    def handle(self, *args, **kwargs):
        old_username = kwargs['old_username']
        new_username = kwargs['new_username']

        try:
            old_user = User.objects.get(username=old_username)
            new_user = User.objects.get(username=new_username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{old_username}" or "{new_username}" does not exist'))
            return

        # Transfer related edges
        Edge.objects.filter(user1=new_user).delete()
        Edge.objects.filter(user2=new_user).delete()

        Edge.objects.filter(user1=old_user).update(user1=new_user)
        Edge.objects.filter(user2=old_user).update(user2=new_user)

        # Update other profiles' references to old_user
        for profile in Profile.objects.filter(strikes=old_user):
            profile.strikes.remove(old_user)
            profile.strikes.add(new_user)

        for profile in Profile.objects.filter(crush=old_user):
            profile.crush = new_user
            profile.save()

        # Delete old user and profile
        old_user.delete()

        self.stdout.write(self.style.SUCCESS(f'Merged accounts: "{old_username}" to "{new_username}"'))
