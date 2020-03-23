from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tutorial import views

urlpatterns = [
    # paths using class-based views
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>', views.SnippetDetail.as_view()),
    path('users/>', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),

    # paths using functional-based views
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),
]

# Append a set of format_suffix_patterns to the existing URLs - works with the format pattern specified in our views
# We don't necessarily need to add these extra url patterns in, but it gives us a simple, clean way of referring to
# a specific format
urlpatterns = format_suffix_patterns(urlpatterns)
