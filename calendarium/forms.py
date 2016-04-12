"""Forms for the ``calendarium`` app."""
from django import forms
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.utils.timezone import datetime, timedelta

from .constants import OCCURRENCE_DECISION_CHOICESS, OCCURRENCE_DECISIONS
from .models import Event, Occurrence


class OccurrenceForm(forms.ModelForm):
    """A form for the ``Occurrence`` model."""
    decision = forms.CharField(
        widget=forms.Select(choices=OCCURRENCE_DECISION_CHOICESS),
    )

    cancelled = forms.BooleanField(
        widget=forms.HiddenInput,
        required=False,
    )

    original_start = forms.DateTimeField(
        widget=forms.HiddenInput,
    )

    original_end = forms.DateTimeField(
        widget=forms.HiddenInput,
    )

    event = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Event.objects.all(),
    )

    class Meta:
        model = Occurrence
        exclude = []

    def save(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['decision'] == OCCURRENCE_DECISIONS['all']:
            changes = dict(
                (key, value) for key, value in iter(cleaned_data.items())
                if value != self.initial.get(key) and self.initial.get(key))
            event = self.instance.event
            # for each field on the event, check for new data in cleaned_data
            for field_name in [field.name for field in event._meta.fields]:
                value = changes.get(field_name)
                if value:
                    setattr(event, field_name, value)
            event.save()

            # repeat for persistent occurrences
            for occ in event.occurrences.all():
                for field_name in [field.name for field in occ._meta.fields]:
                    value = changes.get(field_name)
                    if value:
                        # since we can't just set a new datetime, we have to
                        # adjust the datetime fields according to the changes
                        # on the occurrence form instance
                        if type(value) != datetime:
                            setattr(occ, field_name, value)
                        else:
                            initial_time = self.initial.get(field_name)
                            occ_time = getattr(occ, field_name)
                            delta = value - initial_time
                            new_time = occ_time + delta
                            setattr(occ, field_name, new_time)
                occ.save()

            # get everything from initial and compare to cleaned_data to
            # retrieve what has been changed
            # apply those changes to the persistent occurrences (and the main
            # event)
        elif cleaned_data['decision'] == OCCURRENCE_DECISIONS['this one']:
            self.instance.save()
        elif cleaned_data['decision'] == OCCURRENCE_DECISIONS['following']:
            # get the changes
            changes = dict(
                (key, value) for key, value in iter(cleaned_data.items())
                if value != self.initial.get(key) and self.initial.get(key))

            # change the old event
            old_event = self.instance.event
            end_recurring_period = self.instance.event.end_recurring_period
            old_event.end_recurring_period = self.instance.start - timedelta(
                days=1)
            old_event.save()

            # the instance occurrence holds the info for the new event, that we
            # use to update the old event's fields
            new_event = old_event
            new_event.end_recurring_period = end_recurring_period
            new_event.id = None
            event_kwargs = model_to_dict(self.instance)
            for field_name in [field.name for field in new_event._meta.fields]:
                if (field_name == 'created_by' and
                        event_kwargs.get('created_by')):
                    value = User.objects.get(pk=event_kwargs.get(field_name))
                elif field_name in ['rule', 'category']:
                    continue
                else:
                    value = event_kwargs.get(field_name)
                if value:
                    setattr(new_event, field_name, value)
            new_event.save()
