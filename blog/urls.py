from django.urls import path,include
from .views import *

urlpatterns = [
    # path('',index,name='index'),
    # path('category/<int:pk>/', category_view, name='category'),
    # path('article/<int:pk>/', article_view, name='article'),
    # path('add_article/', add_article, name='add_article'),
    path('',IndexView.as_view(),name='index'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),
    path('category/<int:pk>/',CategoryView.as_view(),name='category'),
    path('add_article/',CreateArticle.as_view(),name='add_article'),
    path('article/<int:pk>/update/',ArticleUpdate.as_view(),name='update'),
    path('article/<int:pk>/delete/',ArticleDelete.as_view(),name='delete'),
    path('login/',user_login,name='login'),
    path('register/',user_register,name='register'),
    path('logout/',user_logout,name='logout'),
    path('save_comment/<int:pk>/',save_comment,name='save_comment'),
    path('profile/<int:pk>/',profile_view,name='profile'),
    path('profile/<int:pk>/edit',ProfileUpdate.as_view(),name='edit'),
    path('fav/<int:pk>/<str:action>/',add_delete_favourite,name='fav')
]
