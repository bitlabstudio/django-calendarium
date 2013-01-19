"""Views for the ``calendarium`` app."""
import calendar

from django.http import Http404
from django.utils.timezone import datetime, timedelta, utc
from django.views.generic import TemplateView

from calendarium.models import Event
from calendarium.utils import monday_of_week


class MonthView(TemplateView):
    """View to return all occurrences of an event for a whole month."""
    template_name = 'calendarium/calendar_month.html'

    def dispatch(self, request, *args, **kwargs):
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        if self.month not in range(1, 13):
            raise Http404
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_month.html'
        return super(MonthView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        month_range = calendar.monthrange(self.year, self.month)
        first = datetime(year=self.year, month=self.month, day=1, tzinfo=utc)
        last = datetime(year=self.year, month=self.month, day=month_range[1],
                        tzinfo=utc)
        occurrences = Event.objects.get_occurrences(first, last)
        ctx = {'object_list': occurrences}
        return ctx


class WeekView(TemplateView):
    """View to return all occurrences of an event for one week."""
    template_name = 'calendarium/calendar_week.html'

    def dispatch(self, request, *args, **kwargs):
        self.week = int(kwargs.get('week'))
        self.year = int(kwargs.get('year'))
        if self.week not in range(1, 52):
            raise Http404
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_week.html'
        return super(WeekView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        monday = monday_of_week(self.year, self.week)
        sunday = monday + timedelta(days=7)
        occurrences = Event.objects.get_occurrences(monday, sunday)
        ctx = {'object_list': occurrences}
        return ctx


class DayView(TemplateView):
    """View to return all occurrences of an event for one day."""
    template_name = 'calendarium/calendar_day.html'

    def dispatch(self, request, *args, **kwargs):
        self.day = int(kwargs.get('day'))
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        if self.month not in range(1, 13):
            raise Http404
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_day.html'
        return super(DayView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        date = datetime(year=self.year, month=self.month, day=self.day,
                        tzinfo=utc)
        occurrences = Event.objects.get_occurrences(date, date)
        ctx = {'object_list': occurrences}
        return ctx
