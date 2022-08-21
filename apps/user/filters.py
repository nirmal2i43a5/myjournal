from django.forms import ModelChoiceField
import django_filters
from django.utils.translation import gettext_lazy as _
from .models import Article
from apps.admin_user.models import Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms.widgets import TextInput ,DateInput
from apps.admin_user.models import Category
from django_filters import DateFilter

class DateInput(DateInput):
    input_type = 'date'
class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name = "title",label="Title",lookup_expr='icontains',widget=TextInput(attrs={'placeholder': 'Enter Title','class':'pr-2'}))
    category = django_filters.ModelChoiceFilter(field_name = "category",label="Category",empty_label="Select Category",
                                                queryset =Category.objects.all(),
                                                )
    # publish_after = DateFilter(field_name="created_at", lookup_expr='gte',label="Published From", widget=DateInput())
    # publish_before = DateFilter(field_name="created_at", lookup_expr='lte',label="Published To",widget=DateInput())
    description = django_filters.CharFilter(field_name = "description",label="Description Tag",lookup_expr='icontains',widget=TextInput(attrs={'placeholder': 'Enter Description Tag','class':'pr-8'}))
    author = django_filters.CharFilter(field_name = "user__normaluser__full_name",lookup_expr='icontains',label = "By Author",
                                       widget=TextInput(attrs={'placeholder': 'Enter Author','class':'pr-2'}))

    # print("Publish _after::: ", publish_after, publish_before)
    class Meta:
        model = Article
        fields = ['title', 'category']
        


