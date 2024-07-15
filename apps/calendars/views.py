from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .forms import *


# Create your views here.
def calendar_view(request):
    form = EventForm()

    context = {"form": form}

    return render(request, "calendars/calendar.html", context=context)


import json

# @login_required
# def event_list(request):
#     events = Event.objects.all()
#     event_list = []

#     for event in events:
#         event_list.append(
#             {
#                 "id": event.id,
#                 "title": event.title,
#                 "start": event.start_date.isoformat(),
#                 "end": event.end_date.isoformat(),
#                 "allDay": event.all_day,
#                 "url": event.event_url,
#             }
#         )
#     return JsonResponse(event_list, safe=False)


# @login_required
# def event_create(request):
#     form = EventForm(request.POST or None)

#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return HttpResponse(status=204)

#     context = {"form": form}

#     return render(request, "calendars/event_form.html", context=context)


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
