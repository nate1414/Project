from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('main', views.main),
    path('logout', views.logout),
    path('main/new', views.new),
    path('new_pokemon', views.new_pokemon),
    path('main/remove/<int:id>', views.remove_poke),
    path('like/<int:id>', views.add_like),
    path('delete/<int:id>', views.delete_comment),
    path('add_comment/<int:id>', views.add_comment),
    path('main/edit/<int:id>', views.edit),
    path('main/edit/<int:id>/update', views.update),
    path('user/<int:id>', views.userprofile),
    path('likedstatus/<int:pokemon_id>', views.likedstatus),
]
