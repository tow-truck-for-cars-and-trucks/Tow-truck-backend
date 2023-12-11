import django_filters as filters
from towin.models import Order


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['istartswith']
        }
