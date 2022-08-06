from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    image = CloudinaryField("avatar",
        overwrite = True,
        blank = True, null=True,
        folder = "avatars/",
        resource_type = "image",
        transformation=[{'width': 150, 'height': 150, 'gravity': "center", 'crop': "thumb"},]
        )

    active = models.BooleanField(default = True)
    pronouns = models.CharField(max_length = 20, null=True, blank=True, default = 'pronouns')
    phone = models.CharField(max_length = 20, null=True, blank=True, default='(xxx) xxx-xxxx\n(or easiest contact)')

    strikes = models.ManyToManyField(User, related_name='strikes')
    crush = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='crush', null=True, blank=True, default=None)
    has_tag_pairing = models.BooleanField(default = False)
    tag_pairing = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='pairing', null=True, blank=True, default=None)
    tag_pairing2 = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='pairing2', null=True, blank=True, default=None)

    def __str__(self):
        return self.user.username


class Edge(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    active = models.BooleanField(default = True)
    weight = models.FloatField(default = 100)

    def __str__(self):
        return (self.user1.username + ' to ' + self.user2.username + ', ' + str(self.weight))

class Pairing(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paired1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paired2')
    user3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paired3', null=True, blank=True, default=None)

    def __str__(self):
        return (self.user1.username + ' with ' + self.user2.username)