from django.views import generic
from rules.contrib.views import PermissionRequiredMixin \
    as RulesPermissionRequiredMixin

"""
Common views.

"""


class PermissionRequiredMixin(RulesPermissionRequiredMixin):

    @property
    def raise_exception(self):
        """Raise authentication error instead of redirecting to login.

        Needed, as permissions for a logged-in user might still be
        limited by the current phase.
        """
        return self.request.user.is_authenticated()


class SortableListView(generic.ListView):
    """Add sorting via request parameter.

    Fields:
        ordering: List containing the single default ordering string
        orderings_supported: List of possible ordering tuples (ordering,
            ordering name)
    """

    ordering = []
    orderings_supported = []

    def dispatch(self, *args, **kwargs):
        ordering = self.request.GET.get('ordering')
        if ordering and ordering in dict(self.orderings_supported):
            self.ordering = [ordering]
        return super().dispatch(*args, **kwargs)

    def get_ordering(self):
        return self.ordering[0]

    def get_ordering_name(self):
        return dict(self.orderings_supported)[self.get_ordering()]