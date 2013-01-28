"""Views for the ``calendarium`` app."""
import calendar

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime, now, timedelta, utc
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from calendarium.forms import OccurrenceForm
from calendarium.models import Event, Occurrence
from calendarium.utils import monday_of_week


class MonthView(TemplateView):
    """View to return all occurrences of an event for a whole month."""
    template_name = 'calendarium/calendar_month.html'

    def dispatch(self, request, *args, **kwargs):
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        if self.month not in range(1, 13):
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                new_date = datetime(self.year, self.month, 1) + timedelta(
                    days=31)
                return HttpResponseRedirect(reverse('calendar_month', kwargs={
                    'year': new_date.year, 'month': new_date.month}))
            elif request.POST.get('previous'):
                new_date = datetime(self.year, self.month, 1) - timedelta(
                    days=1)
                return HttpResponseRedirect(reverse('calendar_month', kwargs={
                    'year': new_date.year, 'month': new_date.month}))
            elif request.POST.get('today'):
                return HttpResponseRedirect(reverse('calendar_month', kwargs={
                    'year': now().year, 'month': now().month}))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_month.html'
        return super(MonthView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        month = [[]]
        week = 0
        for day in calendar.Calendar().itermonthdays(self.year, self.month):
            current = False
            if day:
                date = datetime(year=self.year, month=self.month, day=day,
                                tzinfo=utc)
                occurrences = Event.objects.get_occurrences(date, date)
                if date.date() == now().date():
                    current = True
            else:
                occurrences = []
            month[week].append((day, occurrences, current))
            if len(month[week]) == 7:
                month.append([])
                week += 1
        ctx = {'month': month, 'date': date}
        return ctx


class WeekView(TemplateView):
    """View to return all occurrences of an event for one week."""
    template_name = 'calendarium/calendar_week.html'

    def dispatch(self, request, *args, **kwargs):
        self.week = int(kwargs.get('week'))
        self.year = int(kwargs.get('year'))
        if self.week not in range(1, 53):
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                date = monday_of_week(self.year, self.week) + timedelta(days=7)
                return HttpResponseRedirect(reverse('calendar_week', kwargs={
                    'year': date.year, 'week': date.date().isocalendar()[1]}))
            elif request.POST.get('previous'):
                date = monday_of_week(self.year, self.week) - timedelta(days=7)
                return HttpResponseRedirect(reverse('calendar_week', kwargs={
                    'year': date.year, 'week': date.date().isocalendar()[1]}))
            elif request.POST.get('today'):
                return HttpResponseRedirect(reverse('calendar_week', kwargs={
                    'year': now().year,
                    'week': now().date().isocalendar()[1]}))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_week.html'
        return super(WeekView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        date = monday_of_week(self.year, self.week)
        week = []
        day = 0
        while day < 7:
            current = False
            occurrences = Event.objects.get_occurrences(date, date)
            if date.date() == now().date():
                current = True
            week.append((date, occurrences, current))
            day += 1
            date = date + timedelta(days=1)
        ctx = {'week': week, 'date': date, 'week_nr': self.week}
        return ctx


class DayView(TemplateView):
    """View to return all occurrences of an event for one day."""
    template_name = 'calendarium/calendar_day.html'

    def dispatch(self, request, *args, **kwargs):
        self.day = int(kwargs.get('day'))
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        try:
            self.date = datetime(year=self.year, month=self.month,
                                 day=self.day, tzinfo=utc)
        except ValueError:
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                date = self.date + timedelta(days=1)
                return HttpResponseRedirect(reverse('calendar_day', kwargs={
                    'year': date.year, 'month': date.month, 'day': date.day}))
            elif request.POST.get('previous'):
                date = self.date - timedelta(days=1)
                return HttpResponseRedirect(reverse('calendar_day', kwargs={
                    'year': date.year, 'month': date.month, 'day': date.day}))
            elif request.POST.get('today'):
                return HttpResponseRedirect(reverse('calendar_day', kwargs={
                    'year': now().year, 'month': now().month,
                    'day': now().day}))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_day.html'
        return super(DayView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        occurrences = Event.objects.get_occurrences(self.date, self.date)
        ctx = {'date': self.date, 'occurrences': occurrences}
        return ctx


class EventDetailView(DetailView):
    """View to return information of an event."""
    model = Event


class EventMixin(object):
    """Mixin to handle event-related functions."""
    model = Event

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(EventMixin, self).dispatch(request, *args, **kwargs)


class EventUpdateView(EventMixin, UpdateView):
    """View to update information of an event."""
    pass


class EventCreateView(EventMixin, CreateView):
    """View to create an event."""
    pass


class EventDeleteView(EventMixin, DeleteView):
    """View to delete an event."""
    pass


class OccurrenceViewMixin(object):
    """Mixin to avoid repeating code for the Occurrence view classes."""
    model = Occurrence
    form_class = OccurrenceForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.event = Event.objects.get(pk=kwargs.get('pk'))
        except Event.DoesNotExist:
            raise Http404
        self.index = kwargs.get('index')
        try:
            self.occurrence = self.event.get_occurrences()[self.index]
        except IndexError:
            raise Http404

    def get_queryset(self):
        return self.occurrence


class OccurrenceDeleteView(OccurrenceViewMixin, DeleteView):
    """View to delete an occurrence of an event."""
    pass


class OccurrenceDetailView(OccurrenceViewMixin, DetailView):
    """View to show information of an occurrence of an event."""
    pass


class OccurrenceUpdateView(OccurrenceViewMixin, UpdateView):
    """View to edit an occurrence of an event."""
    pass
