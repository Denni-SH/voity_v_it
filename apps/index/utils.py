from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from apps.user_auth.models import Subscription, User, Friendship


def error_alert(text):
    """
    Warning view
    """
    print('attention!! %s' %text)
    return HttpResponse('<script>alert("ATTENTION!");</script>')

def add_request(who, whom):
    """
    Adding friend request to subscription model view
    """
    if not Subscription.objects.filter(subscriber=who, user=whom).exists() and \
            not Subscription.objects.filter(subscriber=whom, user=who).exists():
        instance = Subscription(subscriber = who, user = whom)
        instance.save()
        return True
    else:
        error_alert('request has`t been created')
        return False

def remove_request(who, whom):
    """
    Removing friend request to subscription model view
    """
    try:
        instance = Subscription.objects.get(subscriber = who, user = whom)
        instance.delete()
    except ObjectDoesNotExist:
        error_alert('request has`t been removed')
        return False
    else:
        return True

def add_friend(cur_user, pk):
    """
    Accepting friend request to friendship model view
    """
    try:
        added_friend = User.objects.get(pk=pk)
    except ObjectDoesNotExist:
        error_alert('user has`t been found')
        return False
    else:
        res = remove_request(added_friend, cur_user)
        if res == True:
            Friendship.make_friend(cur_user, added_friend)
            Friendship.make_friend(added_friend, cur_user)
            return True
        else:
            return False

def remove_friend(cur_user, pk):
    """
    Removing friend from friendship model view
    """
    try:
        owner = Friendship.objects.get(user=cur_user.pk)
        removed_friend = owner.friends.get(pk=pk)
    except ObjectDoesNotExist:
        error_alert('friend has`t been removed')
        return False
    else:
        res = add_request(removed_friend, cur_user)
        if res == True:
            change_status(removed_friend, cur_user)
            Friendship.remove_friend(cur_user, removed_friend)
            Friendship.remove_friend(removed_friend, cur_user)
            return True
        else:
            return False

def change_status(who,whom):
    """
    Changing `is_viewed` status in subscriptions model view
    """
    try:
        instance = Subscription.objects.get(subscriber=who, user=whom)
        if instance.is_viewed == False:
            instance.is_viewed = True
            instance.save()
    except ObjectDoesNotExist:
        error_alert('request status has`t been changed')

