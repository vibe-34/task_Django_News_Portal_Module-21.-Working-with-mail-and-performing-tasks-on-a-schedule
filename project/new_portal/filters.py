from django import forms
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(queryset=Author.objects.all(),
                               field_name='author__user__username',
                               label='Author',
                               empty_label="Выберите автора",
                               lookup_expr='iexact')

    title = CharFilter(field_name='title',
                       label='Title',
                       lookup_expr='iregex')  # icontains не работает без учета регистра именно в SQLite

    time_in = DateFilter(
                        field_name='time_in',
                        widget=forms.DateInput(attrs={'type': 'date'}),
                        label='Дата публикации',
                        lookup_expr='date__gte',)

    class Meta:
        model = Post
        fields = ['author', 'title', 'time_in']
