"""Constants for the ``calendarium`` app."""
from django.utils.translation import ugettext_lazy as _


FREQUENCIES = {
    'YEARLY': 'YEARLY',
    'MONTHLY': 'MONTHLY',
    'WEEKLY': 'WEEKLY',
    'DAILY': 'DAILY',
    'HOURLY': 'HOURLY',
}


FREQUENCY_CHOICES = (
    (FREQUENCIES['YEARLY'], _('Yearly')),
    (FREQUENCIES['MONTHLY'], _('Monthly')),
    (FREQUENCIES['WEEKLY'], _('Weekly')),
    (FREQUENCIES['DAILY'], _('Daily')),
    (FREQUENCIES['HOURLY'], _('Hourly')),
)
