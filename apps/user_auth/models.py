from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class User(AbstractUser):
    birth_date = models.DateField(null = True, blank = True)
    locality = models.CharField(max_length = 40, blank = True)
    phone = models.CharField(max_length = 20, blank = True)
    avatar = models.ImageField(blank = True, default='default_user.jpeg')
    thumbnail = models.ImageField(blank = True, default='default_user.jpeg')

    def save(self, *args, **kwargs):
        if self.avatar:
            img = Image.open(self.avatar)
            output = BytesIO()
            img = img.resize((195, 195))
            img.save(output,format='PNG', quality=100)
            # change the imagefield value to be the newley modifed image value
            self.thumbnail = InMemoryUploadedFile(output,
                                               'ImageField',
                                               "%s.jpg" % self.thumbnail.name.split('.')[0],
                                               'image/jpeg',
                                               sys.getsizeof(output),
                                               None)
            super(User, self).save()


class Subscription(models.Model):
    timestamp = models.DateTimeField(auto_now = True, editable = False)
    user = models.ForeignKey(User, related_name = 'following')
    subscriber = models.ForeignKey(User, related_name = 'creator')
    is_viewed = models.BooleanField(default = False)

    def __str__(self):
        return self.subscriber.username + ' -> ' + self.user.username


class Friendship(models.Model):
    timestamp = models.DateTimeField(auto_now = True, editable = False)
    user = models.ForeignKey(User, related_name = 'user')
    friends = models.ManyToManyField(User, default=None)

    @classmethod
    def make_friend(self, user, new_friend):
        friend, created = self.objects.get_or_create(user = user)
        friend.friends.add(new_friend)

    @classmethod
    def remove_friend(self, user, new_friend):
        friend, created = self.objects.get_or_create(user = user)
        friend.friends.remove(new_friend)

    def __str__(self):
        return self.user.username


