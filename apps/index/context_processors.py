from apps.user_auth.models import Subscription
from apps.chat.models import Message

def side_bar_context(request):
    """
    Processor for side-bar`s pills
    """
    context_dict = dict()
    new_followers = Subscription.objects.filter(user=request.user.pk, is_viewed=False)
    context_dict['new_followers_count'] = len(new_followers)
    return context_dict
