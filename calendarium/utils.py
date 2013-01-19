"""
Utils for the ``calendarium`` app.

The code of these utils is highly influenced by or taken from the utils of
django-schedule:

https://github.com/thauber/django-schedule/blob/master/schedule/utils.py


"""
import time
from django.utils import timezone


def now(**kwargs):
    """
    Utility function to zero microseconds to avoid inaccuracy.

    I replaced the microseconds, because there is some slightly varying
    difference that occurs out of unknown reason. Since we probably never
    schedule events on microsecond basis, seconds and microseconds will be
    zeroed everywhere.

    """
    return timezone.now(**kwargs).replace(second=0, microsecond=0)


def monday_of_week(year, month):
    """
    Returns a datetime for the monday of the given week of the given year.

    """
    str_time = time.strptime('{0} {1} 1'.format(year, month), '%Y %W %w')
    return timezone.datetime(year=str_time.tm_year, month=str_time.tm_mon,
                             day=str_time.tm_mday, tzinfo=timezone.utc)


class OccurrenceReplacer(object):
    """
    When getting a list of occurrences, the last thing that needs to be done
    before passing it forward is to make sure all of the occurrences that
    have been stored in the datebase replace, in the list you are returning,
    the generated ones that are equivalent.  This class makes this easier.

    """
    def __init__(self, persisted_occurrences):
        lookup = [
            ((occ.event, occ.original_start, occ.original_end), occ) for
            occ in persisted_occurrences]
        self.lookup = dict(lookup)

    def get_occurrence(self, occ):
        """
        Return a persisted occurrences matching the occ and remove it from
        lookup since it has already been matched
        """
        return self.lookup.pop(
            (occ.event, occ.original_start, occ.original_end),
            occ)

    def has_occurrence(self, occ):
        return (occ.event, occ.original_start, occ.original_end) in self.lookup

    def get_additional_occurrences(self, start, end):
        """
        Return persisted occurrences which are now in the period
        """
        return [occ for key, occ in self.lookup.items() if (
            occ.start < end and occ.end >= start and not occ.cancelled)]
