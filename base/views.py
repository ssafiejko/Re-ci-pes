from django.shortcuts import render, redirect
from .models import Recipe, Topic, Comment, User
from django.contrib.auth import authenticate, login, logout
from .forms import RecipeForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.urls import path
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration :(')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    recipes = Recipe.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    recipe_count = recipes.count()
    comments = Comment.objects.filter(Q(recipe__topic__name__icontains=q))
    context = {'recipes': recipes, 'topics': topics, 'recipe_count': recipe_count, 'comments': comments}

    return render(request, 'base/home.html', context)


def recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)

    comments = recipe.comment_set.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            recipe=recipe,
            body=request.POST.get('body')
        )
        return redirect('recipe', pk=recipe.id)

    context = {'recipe': recipe, 'comments': comments}
    return render(request, 'base/recipe.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    recipes = user.recipe_set.all()
    comments = user.comment_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'recipes': recipes, 'comments': comments, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRecipe(request):
    form = RecipeForm(request.POST, request.FILES)
    topics = Topic.objects.all()


    if request.method == 'POST':
        recipe_image = request.FILES.get('recipe_image')

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        recipe = Recipe.objects.create(
            autor=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            recipe_image=request.FILES.get('recipe_image'),
            text=request.POST.get('text'),

        )
        recipe.save()
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()

        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/recipe_form.html', context)


@login_required(login_url='login')
def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    topics = Topic.objects.all()

    form = RecipeForm(instance=recipe)
    if request.user != recipe.autor:
        return HttpResponse('You are not allowed to do this!')

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        recipe.name = request.POST.get('name')
        recipe.description = request.POST.get('description')
        recipe.topic = topic
        recipe.text = request.POST.get('text')
        recipe.recipe_image = request.FILES.get('recipe_image')
        recipe.save()

        if form.is_valid():
            form.save()

    context = {'form': form, 'topics': topics, 'recipe': recipe}

    return render(request, 'base/recipe_form.html', context)


@login_required(login_url='login')
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.user != recipe.autor:
        return HttpResponse('You are not allowed to do this!')

    if request.method == "POST":
        recipe.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': recipe})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})

