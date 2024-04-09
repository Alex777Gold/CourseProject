from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Mission, Subscription


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mission_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def mission_list(request):
    if 'search' in request.GET:
        search_query = request.GET['search']
        # filtering by seach query all fied also with date
        missions = Mission.objects.filter(name__icontains=search_query) | Mission.objects.filter(
            launch_date__icontains=search_query) | Mission.objects.filter(mission_type__icontains=search_query) | Mission.objects.filter(country__icontains=search_query)
    else:
        missions = Mission.objects.all()
    return render(request, 'missions/mission_list.html', {'missions': missions})


def subscriptions(request):
    if request.user.is_authenticated:
        subscriptions = Subscription.objects.filter(user=request.user)
        return render(request, 'subscriptions.html', {'subscriptions': subscriptions})
    else:
        return redirect('login')


def subscribe(request, mission_id):
    if request.user.is_authenticated:
        mission = Mission.objects.get(id=mission_id)
        subscription, created = Subscription.objects.get_or_create(
            user=request.user, mission=mission)
        if created:
            messages.success(request, 'Ви успішно підписалися на місію!')
            return JsonResponse({'status': 'success', 'msg': 'Ви успішно підписалися'})
        else:
            messages.info(request, 'Ви вже підписані на цю місію!')
            return JsonResponse({'status': 'info', 'msg': 'Ви вже підписані на цю місію!'})


def unsubscribe(request, mission_id):
    if request.user.is_authenticated:
        mission = Mission.objects.get(id=mission_id)
        subscription = Subscription.objects.filter(
            user=request.user, mission=mission)
        if subscription.exists():
            subscription.delete()
            messages.success(request, 'Ви успішно відписалися від місії!')
        else:
            messages.info(request, 'Ви не підписані на цю місію!')
        return JsonResponse({'status': 'success', 'msg': 'Ви успішно відписалися'})
