from django.urls import path
from .views import SkillListView, SkillCreateView

urlpatterns = [
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('skills/create/', SkillCreateView.as_view(), name='skill-create'),
]
