from apps.user.views import *
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('register/',user_register,name='register'),
    path('upload-article/',upload_article,name='upload-article'),
    path('article-view/<pk>/',article_view,name='article-view'),
    path('article-update/<pk>/',article_update_view,name='article-update'),
    path('article-delete/<pk>/',article_delete_view,name='article-delete'),
    path('article-under-review/', article_under_review, name='article-under-review'),
    path('article-accepted/', accepted_article_list, name='article-accepted'),
    path('article-rejected/', rejected_article_list, name='article-rejected'),
    # path('article_detail/<int:pk>/',ArticleDetailView.as_view(),name="article_detail"),
    path('article_detail/<pk>/',article_detail_view,name="article_detail"),
]



