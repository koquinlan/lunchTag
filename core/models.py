from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    strikes = models.ManyToManyField(User, related_name='strikes')

    def __str__(self):
        return self.user.username


class Edge(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    weight = models.IntegerField()

    def __str__(self):
        return (self.user1.username + ' to ' + self.user2.username + ', ' + str(self.weight))