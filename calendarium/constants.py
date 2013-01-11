"""Constants for the ``calendarium`` app."""
from django.utils.translation import ugettext_lazy as _


FREQUENCIES = {
    'YEARLY': 'Yearly',
    'MONTHLY': 'Monthly',
    'WEEKLY': 'Weekly',
    'DAILY': 'Daily',
    'HOURLY': 'Hourly',
    'MINUTELY': 'Minutely',
    'SECONDLY': 'Secondly'
}


FREQUENCY_CHOICES = (
    (FREQUENCIES['YEARLY'], _('Yearly')),
    (FREQUENCIES['MONTHLY'], _('Monthly')),
    (FREQUENCIES['WEEKLY'], _('Weekly')),
    (FREQUENCIES['DAILY'], _('Daily')),
    (FREQUENCIES['HOURLY'], _('Hourly')),
    (FREQUENCIES['MINUTELY'], _('Minutely')),
    (FREQUENCIES['SECONDLY'], _('Secondly'))
)
