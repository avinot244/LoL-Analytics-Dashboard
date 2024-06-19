from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

import json

@api_view(["POST"])
def loginUser(request):
    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse({"detail":"Please provide credentials"})
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return JsonResponse({"detail":"Invalid credentials"}, status=400)

    login(request, user)
    return JsonResponse({"detail":"Successfully loed in !"})

def logoutUser(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You are not logged in"}, status=400)
    logout(request)
    return JsonResponse({"detail": "Successfully logged out"})

@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})
    return JsonResponse({"isauthenticated": True})

def whomai_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})
    return JsonResponse({"username": request.user.username})

@api_view(['GET'])
def getUserList(request):
    query = User.objects.all()
    for res in query:
        print(res)

    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteUser(request, username : str):
    toDelete = User.objects.get(username__exact=username)
    toDelete.delete()
    return Response(status=status.HTTP_200_OK)
