from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt, requests, pokebase

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        first_name = request.POST['first_name'], 
        last_name = request.POST['last_name'], 
        email = request.POST['email'], 
        username = request.POST['username'],
        password = pw_hash
    )

    request.session['user_id'] = user.id
    return redirect('/main')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(username=request.POST['username'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/main')
    return redirect('/')

def main(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'pokemons': NewPokemonIdea.objects.all(),
            'comment' : Comment.objects.all(),
        }
        return render(request, 'main.html', context)
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def new(request):
    if 'user_id' in request.session:
        context = {
            'pokemon': NewPokemonIdea.objects.all(),
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'new.html', context)
    return redirect('/')

def new_pokemon(request):
    errors = NewPokemonIdea.objects.pokemon_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    user = User.objects.get(id=request.session['user_id'])
    pokemon = NewPokemonIdea.objects.create(
        pokemon = request.POST['pokemon'],
        types = request.POST['types'],
        desc = request.POST['desc'],
        creator = user,
    )
    return redirect('/main')

def remove_poke(request, id):
    if 'user_id' in request.session:
        removed = NewPokemonIdea.objects.get(id=id)
        removed.delete()
        return redirect('/main')
    return redirect('/')

def add_like(request, id):
    user_liked = User.objects.get(id=request.session['user_id'])
    liked_post = NewPokemonIdea.objects.get(id=id)
    liked_post.user_likes.add(user_liked)
    return redirect('/main')

def add_comment(request, id):
    creator = User.objects.get(id=request.session['user_id'])
    pokemon = NewPokemonIdea.objects.get(id=id)
    Comment.objects.create(
        comment = request.POST['comment'],
        creator = creator,
        newpokemonidea_message = pokemon
        )
    return redirect('/main')

def delete_comment(request, id):
    deleted = Comment.objects.get(id=id)
    deleted.delete()
    return redirect('/main')

def edit(request, id):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'pokemon': NewPokemonIdea.objects.get(id=id)
        }
        return render(request, 'edit_post.html', context)
    return redirect('/')

def update(request, id):
    errors = NewPokemonIdea.objects.pokemon_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    if 'user_id' in request.session:
        edit_post = NewPokemonIdea.objects.get(id=id)
        edit_post.pokemon = request.POST.get('pokemon')
        edit_post.types = request.POST.get('types')
        edit_post.desc = request.POST.get('desc')
        edit_post.save()
        return redirect('/main')
    return redirect('/')

def userprofile(request, id):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'pokemon': NewPokemonIdea.objects.all()
        }
        return render(request, 'userprofile.html', context)
    return redirect('/')

def likedstatus(request, pokemon_id):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'pokemons': NewPokemonIdea.objects.filter(id=pokemon_id)
        }
        return render(request, 'likedstatus.html', context)
    return redirect('/')