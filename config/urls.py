from django.contrib import admin
from django.urls import path, include

from ui.views import query_llm

urlpatterns = [
    path("", include('ui.urls')),
    path('query_llm/', query_llm, name='query_llm'),
    path("__reload__/", include("django_browser_reload.urls")),

]