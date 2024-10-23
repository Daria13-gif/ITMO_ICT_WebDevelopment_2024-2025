from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Conference, Review, Participant
from .forms import NewUserForm, ReviewForm, ParticipantForm, ConferenceForm, CustomAuthenticationForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'project_first_app/login.html'  # Убедитесь, что путь к вашему шаблону правильный
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        return super().form_valid(form)

# Главная страница
class HomeView(ListView):
    model = Conference
    template_name = 'project_first_app/home.html'
    context_object_name = 'conferences'

# Регистрация пользователя
class RegisterView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'project_first_app/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()  # Пароль будет автоматически хэширован
        login(self.request, user)  # Аутентифицируем пользователя после регистрации
        return redirect(self.success_url)

# Отзывы к конференциям
class AddReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'project_first_app/add_review.html'

    def form_valid(self, form):
        # Получаем текущего пользователя как экземпляр модели User
        user = get_user_model().objects.get(pk=self.request.user.pk)
        form.instance.user = user  # связываем с текущим пользователем
        form.instance.conference_id = self.kwargs['conference_id']  # добавляем конференцию
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conference'] = get_object_or_404(Conference, pk=self.kwargs['conference_id'])  # передаем конференцию
        return context


# Регистрация на конференцию
class RegisterParticipantView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'project_first_app/author_registration.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # связываем с текущим пользователем
        return super().form_valid(form)

# Список участников конференции
class ParticipantListView(ListView):
    model = Participant
    template_name = 'project_first_app/participants.html'
    context_object_name = 'participants'

    def get_queryset(self):
        return Participant.objects.all()  # Возвращаем всех участников

# Функция для отображения деталей конференции
class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'project_first_app/conference.html'
    context_object_name = 'conference'

# Создание новой конференции
class NewConferenceView(CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'project_first_app/new_conference.html'
    success_url = reverse_lazy('home')

# Редактирование конференции
class EditConferenceView(UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'project_first_app/edit_conference.html'
    success_url = reverse_lazy('home')

# Удаление конференции
class DeleteConferenceView(DeleteView):
    model = Conference
    template_name = 'project_first_app/delete_conference.html'
    success_url = reverse_lazy('home')

# Детали участника
class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'project_first_app/participant_detail.html'
    context_object_name = 'participant'

# Новый участник
class NewParticipantView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'project_first_app/new_participant.html'
    success_url = reverse_lazy('home')

class ConferenceListView(ListView):
    model = Conference
    template_name = 'project_first_app/conference_list.html'
    context_object_name = 'conferences'

class ReviewListView(ListView):
    model = Review
    template_name = 'project_first_app/review_list.html'
    context_object_name = 'reviews'

class AuthorRegistrationView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'project_first_app/author_registration.html'
    success_url = reverse_lazy('home')  # Перенаправление после успешной регистрации


class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'project_first_app/edit_participant.html'

    def get_success_url(self):
        return reverse_lazy('participant-list')


class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'project_first_app/delete_participant.html'

    def get_success_url(self):
        return reverse_lazy('participant-list')


class RegisterParticipantView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'project_first_app/author_registration.html'

    def get(self, request):
        # Получаем список всех конференций
        conferences = Conference.objects.all()

        # Получаем регистрации текущего пользователя
        my_participants = Participant.objects.filter(user=request.user)

        return render(request, 'project_first_app/author_registration.html', {
            'conferences': conferences,  # Передаем список конференций
            'my_participants': my_participants  # Передаем регистрации пользователя
        })

    def post(self, request):
        conference_id = request.POST.get('conference')
        conference = get_object_or_404(Conference, id=conference_id)

        # Проверяем, не зарегистрирован ли пользователь уже на эту конференцию
        if Participant.objects.filter(user=request.user, conference=conference).exists():
            return render(request, 'project_first_app/author_registration.html', {
                'error': 'Вы уже зарегистрированы на эту конференцию',
                'conferences': Conference.objects.all(),
                'my_participants': Participant.objects.filter(user=request.user)
            })

        # Если нет, создаем новую регистрацию
        Participant.objects.create(user=request.user, conference=conference)
        return redirect('my_participants')


class UserParticipantListView(ListView):
    model = Participant
    template_name = 'project_first_app/user_participants.html'
    context_object_name = 'participants'

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user)

class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'project_first_app/edit_participant.html'

    def get_queryset(self):
        # Ограничиваем редактирование регистраций только пользователю, который их создал
        return Participant.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('my_participants')  # Возвращаем пользователя на список его регистраций после успешного редактирования

class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'project_first_app/delete_participant.html'

    def get_queryset(self):
        # Ограничиваем удаление регистраций только пользователю, который их создал
        return Participant.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('my_participants')  # Возвращаем пользователя на список его регистраций после успешного удаления



