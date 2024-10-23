from django.urls import path
from .views import (
    RegisterView,
    AddReviewView,
    RegisterParticipantView,
    ParticipantListView,
    ConferenceDetailView,
    DeleteConferenceView,
    EditConferenceView,
    NewConferenceView,
    NewParticipantView,
    HomeView,
    ParticipantDetailView,
    ConferenceListView,
    ReviewListView,
    AuthorRegistrationView,
    ParticipantUpdateView,
    ParticipantDeleteView,
    UserParticipantListView,
)
from django.contrib.auth.views import LoginView, LogoutView  # Добавляем LoginView и LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Главная страница
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('login/', LoginView.as_view(template_name='project_first_app/login.html'), name='login'),  # Вход в систему
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Выход из системы
    path('add_review/<int:conference_id>/', AddReviewView.as_view(), name='add_review'),  # Добавление отзыва
    path('register_participant/<int:conference_id>/', RegisterParticipantView.as_view(), name='register_participant'),  # Регистрация участника
    path('participants/<int:conference_id>/', ParticipantListView.as_view(), name='participants'),  # Список участников конференции
    path('conference/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),  # Детали конференции
    path('conference/new/', NewConferenceView.as_view(), name='new_conference'),  # Новая конференция
    path('conference/<int:pk>/edit/', EditConferenceView.as_view(), name='edit_conference'),  # Редактирование конференции
    path('conference/<int:pk>/delete/', DeleteConferenceView.as_view(), name='delete_conference'),  # Удаление конференции
    path('participant/<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),  # Детали участника
    path('participant/new/', NewParticipantView.as_view(), name='new_participant'),  # Новый участник
    path('conferences/', ConferenceListView.as_view(), name='conference-list'),  # Список конференций
    path('reviews/', ReviewListView.as_view(), name='review-list'),  # Список отзывов
    path('participants/', ParticipantListView.as_view(), name='participant-list'),  # Список всех участников
    path('author/register/', AuthorRegistrationView.as_view(), name='author-registration'),  # Регистрация автора
    path('participant/<int:pk>/edit/', ParticipantUpdateView.as_view(), name='edit_participant'),
    path('participant/<int:pk>/delete/', ParticipantDeleteView.as_view(), name='delete_participant'),
    path('my_participants/', UserParticipantListView.as_view(), name='my_participants'),
]
