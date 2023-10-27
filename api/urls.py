from django.urls import path

from .views import *

# Book History


urlpatterns = [
    # Book
    path('book/', BookListCreateView.as_view(), name='book-list-create'),
    path('book/list', BookListCreateView.as_view(), name='book-list-create'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    #
    # Book History
    path('bookhistory/', BookHistoryListCreateView.as_view(), name='bookhistory-list-create'),
    path('bookhistory/list', BookHistoryListCreateView.as_view(), name='bookhistory-list-create'),
    path('bookhistory/<int:pk>/', BookHistoryListCreateView.as_view(), name='bookhistory-detail'),
    #
    # Book Review
    path('bookreview/', BookReviewListCreateView.as_view(), name='bookreview-list-create'),
    path('bookreview/list', BookReviewListCreateView.as_view(), name='bookreview-list-create'),
    path('bookreview/<int:pk>/', BookReviewDetailView.as_view(), name='bookreview-detail'),

    # user
    path('user/register/', RegisterView.as_view()),
    path('user/login/', LoginView.as_view()),
    path('user/user/', UserView.as_view()),
    path('user/logout/', LogoutView.as_view())

]
