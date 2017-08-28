# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Player


def index(request):
    return HttpResponse("Hello, world. You're at the golfsetup index.")

def players(request):
    players_list = get_list_or_404(Player.objects.order_by('name'))
    return render(request, 'golfsetup/index.html', {'players_list': players_list})


def player(request, player_id):
    thisplayer = get_object_or_404(Player, pk=player_id)
    return render(request, 'golfsetup/player.html', {'player': thisplayer})


def tournament(request, tournament_id):
    response = "You're looking at tournament question %s."
    return HttpResponse(response % tournament_id)
