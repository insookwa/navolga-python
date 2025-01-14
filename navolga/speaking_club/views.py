from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Attendee

def event_list(request):
    events = Event.objects.order_by('date', 'time').filter(date__gte='today')
    return render(request, 'speaking_club/speaking_club.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    attendees = event.attendees.count()
    return render(request, 'speaking_club/event_detail.html', {'event': event, 'attendees': attendees})

@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.attendees.count() >= event.max_attendees:
        return render(request, 'speaking_club/event_full.html', {'event': event})
    Attendee.objects.get_or_create(user=request.user, event=event)
    return redirect('event_detail', pk=event.pk)
