from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from apps.user_auth.models import User

# @login_required
class SearchView(ListView):
    """
    Searching users view
    """
    template_name = 'results.html'
    model = User
    paginate_by = 12
    context_object_name = 'results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.strip('').strip(' ').split(' ')
            users = User.objects.none()
            for q in query_list:
                users = users | result.filter(first_name=q) | result.filter(last_name=q)
            result= users
        return result