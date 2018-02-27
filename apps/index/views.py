from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.generic import UpdateView, ListView
from django.http import HttpResponseRedirect
from apps.index.forms import SettingsForm
from apps.index import utils
from apps.user_auth.models import User, Friendship, Subscription


def personal_page(request,pk):
    """
    Personal page view
    """
    if request.user.is_authenticated():
        if User.objects.filter(pk=pk):
            user_page = User.objects.get(pk=pk)
        else:
            return HttpResponseRedirect("/id=%s/" % request.user.pk)

        users = User.objects.all()

        if Friendship.objects.filter(pk = request.user.pk):
            friendship_user = Friendship.objects.get(user=request.user.pk, pk = request.user.pk)
        else:
            now_user = User.objects.get(pk=request.user.pk)
            friendship_user = Friendship.objects.create(user=now_user, pk=request.user.pk)
        friends = friendship_user.friends.all()
        followers = Subscription.objects.filter(user = request.user)
        followers_list = followers.values_list('subscriber', flat = True).distinct()
        following = Subscription.objects.filter(subscriber = request.user)
        # "flat = True" means results are values: 1 ; "flat = False" - results are one-valued-tuples: (1,)
        following_list = following.values_list('user', flat = True).distinct()


        return render(request, 'index.html', {'user_page': user_page,
                                              'users': users,
                                              'friends': friends,
                                              'followers': followers_list,
                                              'following': following_list,
                                              'subs': followers
                                              }
                      )
    else:
        return HttpResponseRedirect("/account/login/")

def index(request):
    """
    Redirecting from root url view
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/id=%s/' %request.user.pk)
    else:
        return HttpResponseRedirect("/account/login/")


class EditUserInfo(UpdateView):
    """
    Settings page view
    """
    template_name = 'settings.html'
    form_class = SettingsForm
    context_object_name = 'user_info'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('PersonalPage', kwargs={'pk': self.request.user.pk})



class FriendsList(ListView):
    """
    Friends page view
    """
    template_name = 'friends.html'
    model = Friendship
    context_object_name = 'friends'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_object, created = Friendship.objects.get_or_create(user=self.request.user.pk)

        followers = Subscription.objects.filter(user=self.request.user.pk)
        old_followers = followers.filter(is_viewed=True)
        new_followers = followers.filter(is_viewed=False)

        following = Subscription.objects.filter(subscriber=self.request.user.pk)

        context['friends'] = [friend for friend in friend_object.friends.all() if friend != self.request.user.pk]
        context['followers'] = old_followers
        context['new_followers'] = new_followers
        context['following'] = following

        context['count_friends'] = len(context['friends'])
        context['count_followers'] = len(Subscription.objects.filter(user=self.request.user.pk))
        context['new_count'] = len(context['new_followers'])
        context['count_following'] = len(Subscription.objects.filter(subscriber=self.request.user.pk))

        return context


@login_required
def add_or_remove_friend_request(request, pk, operation):
    """
    Friendship requests operations view
    """
    try:
        who = get_object_or_404(User, pk = request.user.pk)
        whom = get_object_or_404(User, pk = pk)
    except ObjectDoesNotExist:
        utils.error_alert('user has`t been found')
    else:
        if operation == 'add':
            utils.add_request(who, whom)
        else:
            utils.remove_request(who, whom)
    finally:
        return HttpResponseRedirect("/friends/")

@login_required
def add_or_remove_friend(request, pk, operation):
    """
    Add and remove friends view
    """
    try:
        cur_user = get_object_or_404(User, pk = request.user.pk)
    except ObjectDoesNotExist:
        utils.error_alert('user has`t been found')
    else:
        if operation == 'add':
            utils.add_friend(cur_user, pk)
        else:
            utils.remove_friend(cur_user, pk)
    finally:
        return HttpResponseRedirect("/friends/")

@login_required
def leave_in_subscribers(request, pk):
    """
    Leave user in subscribers view
    """
    try:
        who = get_object_or_404(User, pk = request.user.pk)
        whom = get_object_or_404(User, pk = pk)
    except:
        utils.error_alert('user has`t been found')
    else:
        utils.change_status(whom,who)
    finally:
        return HttpResponseRedirect("/friends/")
