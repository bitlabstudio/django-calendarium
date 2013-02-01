"""Constants for the ``calendarium`` app."""
from django.utils.translation import ugettext_lazy as _


FREQUENCIES = {
    'YEARLY': 'YEARLY',
    'MONTHLY': 'MONTHLY',
    'WEEKLY': 'WEEKLY',
    'DAILY': 'DAILY',
}


FREQUENCY_CHOICES = (
    (FREQUENCIES['YEARLY'], _('Yearly')),
    (FREQUENCIES['MONTHLY'], _('Monthly')),
    (FREQUENCIES['WEEKLY'], _('Weekly')),
    (FREQUENCIES['DAILY'], _('Daily')),
)


OCCURRENCE_DECISIONS = {
    'all': 'all',
    'following': 'following',
    'this one': 'this one',
}

OCCURRENCE_DECISION_CHOICESS = (
    (OCCURRENCE_DECISIONS['all'], _('all')),
    (OCCURRENCE_DECISIONS['following'], _('following')),
    (OCCURRENCE_DECISIONS['this one'], _('this one')),
)
