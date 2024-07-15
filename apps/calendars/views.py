from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import *
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
def calendar_view(request):
    form = EventForm()

    context = {"form": form}

    return render(request, "calendars/calendar.html", context=context)


import json

@login_required
def event_list(request):
    events = Event.objects.all()
    event_list = []

    for event in events:
        event_list.append(
            {
                "id": event.id,
                "title": event.title,
                "start": event.start_date.isoformat(),
                "end": event.end_date.isoformat(),
                "allDay": event.all_day,
                "url": event.event_url,
                "extendedProps":{
                    "calendar": event.label,
                    "description": event.description,
                    "location": event.location
                }
            }
        )
    return JsonResponse(event_list, safe=False)

@csrf_exempt    
@login_required
def event_create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = EventForm(data)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            print (user)
            form.instance.user = user
            form.save()
            return JsonResponse({"message": "Event created successfully"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return HttpResponse(status=405) 

@csrf_exempt
@login_required
def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "PUT":
        data = json.loads(request.body)
        form = EventForm(data, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Event updated successfully"}, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return HttpResponse(status=405) 


@csrf_exempt
@login_required
def event_delete(request, id):
    if request.method == "DELETE":
        event = get_object_or_404(Event, id=id)
        event.delete()
        return JsonResponse({"message": "Event deleted successfully"}, status=204)
    return HttpResponse(status=405)  
# @login_required
# def event_update(request, id):
#     event = get_object_or_404(Event, id=id)
#     form = EventForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return HttpResponse(status=204)

#     context = {"form": form, "event": event}

#     return render(request, "calendars/event_form.html", context=context)


# @login_required
# def event_delete(request, id):
#     event = get_object_or_404(Event, id=id)
#     event.delete()

#     return HttpResponse(status=204)
