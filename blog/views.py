from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from .models import Article,Category,Comment,Profile,Favourite
from .forms import ArticleForm, LoginForm, RegisterForm, CommentForm, ProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login,logout
from django.contrib import messages

# Create your views here.

# def index(request):
#     articles = Article.objects.all()
#     context = {
#         'title': 'Главная страница Блог',
#         'articles':articles
#     }
#
#     return render(request,'blog/index.html',context)

class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    extra_context = {
        'title': "Главная страница Блог"
    }


# def category_view(request,pk):
#     category = Category.objects.get(pk=pk)
#     articles = Article.objects.filter(category=category)
#     context = {
#         'articles': articles,
#         'title': f"Категория: {category.title}"
#     }
#     return render(request,'blog/index.html',context)

class CategoryView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "blog/index.html"

    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context



# def article_view(request,pk):
#     article = Article.objects.get(pk=pk)
#
#     context = {
#         'article': article,
#         'title': f'Статья: {article.title}'
#
#     }
#     return render(request,'blog/article.html',context)

class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(article=article)
        context['comments'] = comments
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['title'] = f'Статья: {article.title}'
        return context

def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('article', article.pk)
    else:
        form = ArticleForm()

    context = {
        'title':'Создание новой статьи',
        'form': form
    }
    return render(request,'blog/article_form.html',context)

class CreateArticle(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'Create an article'
    }

class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'Edit an article'
    }


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request,user)
                messages.success(request,'Authorization successfull')
                return redirect('index')
            else:
                messages.error(request,'Entered password or login is incorrect')
                return redirect('login')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Sign in'
    }
    return render(request,'blog/user_form.html',context)

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            messages.success(request,'Signed up successfull. Sign in to your account')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request,form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegisterForm()

    context ={
        'form': form,
        'title': 'Регистрация пользователя'
    }
    return render(request,'blog/user_form.html',context)

def user_logout(request):
    logout(request)
    return redirect('index')


def save_comment(request,pk):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article= Article.objects.get(pk=pk)
            comment.user = request.user
            comment.save()
            return redirect('article',pk)

def profile_view(request,pk):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    favs = Favourite.objects.filter(user=user)
    articles = [i.article for i in favs]

    context = {
        'profile':profile,
        'title': 'Страница пользователя',
        'articles': articles
    }
    return render(request,'blog/profile.html',context)


class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'blog/user_form.html'
    extra_context = {
        'title':'Изменение профиля'
    }


def add_delete_favourite(request,pk,action):
    user = request.user
    article = Article.objects.get(pk=pk)

    if action == 'add':
        favourite = Favourite.objects.create(user=user,article=article)
        favourite.save()
    else:
        favourite = Favourite.objects.get(user=user,article=article)
        favourite.delete()
    return redirect('index')
