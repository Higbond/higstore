from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .models import Course, Lesson, Comment # Подключаем модель Comment
from .forms import CommentForm # Подключаем класс формы для Comment
# from cloudipsp import Api, Checkout
import time
import json

secret_key = 'test'


def callback_payment(request):
    if request.method == 'POST':
        data = json.load(request.POST)

        print(data)


def tarrifsPage(request):
    # api = Api(merchant_id=1396424,
    #           secret_key=secret_key)
    # checkout = Checkout(api=api)
    # data = {
    #     "currency": "USD",
    #     "amount": 1500,
    #     "order_desc": "Покупка подписки на сайте",
    #     "order_id": str(time.time()),
    #     "merchant_data": 'example@itproger.com'
    # }
    # url = checkout.url(data).get('checkout_url')
    url = ''
    return render(request, 'courses/tarrifs.html', {'title': 'Тарифы на сайте', 'url': url})


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        return ctx


class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['title'] = course
        ctx['lessons'] = Lesson.objects.filter(course=course).order_by('number')
        return ctx


class LessonDetailPage(DetailView):
    model = Course
    template_name = 'courses/lesson-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = Lesson.objects.filter(slug=self.kwargs['lesson_slug']).first()

        lesson.video = lesson.video.split("=")[1]

        # Передаем в шаблон все комментарии, что соответсвуют id записи, на которой мы находимся
        comments = Comment.objects.filter(lesson=lesson.id).all()
        ctx['comments'] = comments
        # Также передаем форму в шаблон
        ctx['commForm'] = CommentForm()

        ctx['title'] = lesson
        ctx['lesson'] = lesson
        return ctx

    # Этот метод срабатывает при отправке данных из формы
    def post(self, request, *args, **kwargs):
        # Получаем курс и получаем текущий урок
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = Lesson.objects.filter(course=course).filter(slug=self.kwargs['lesson_slug']).first()

        post = request.POST.copy()  # Копируем POST данные прежде, чем их валидировать
        post['user'] = request.user  # Устаналвиаем свои данные – указываем авторизованного пользователя
        post['lesson'] = lesson  # Указываем урок, на котором сейчас находимся
        request.POST = post  # Меняем request.POST данные на новые, измененные данные

        # Создаем объект на основе класса формы
        form = CommentForm(request.POST)
        if form.is_valid():  # Проверяем его
            form.save()  # Сохраняем новый комментарий

        # Выполняем переадресацию
        url = self.kwargs['slug'] + '/' + self.kwargs['lesson_slug']

        return redirect('/course/' + url)
