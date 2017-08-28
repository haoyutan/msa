"""
Copied and modified from django-rest-framework/rest_framework/utils/encoders.py
"""
import datetime, decimal, json, uuid

from django.db.models.query import QuerySet
from django.utils import six, timezone
from django.utils.encoding import force_text
from django.utils.functional import Promise

from rest_framework.compat import coreapi, total_seconds


class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time/timedelta,
    decimal types, generators and other basic python objects.
    """
    def default(self, obj):
        # For Date Time string spec, see ECMA 262
        # http://ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
        if isinstance(obj, datetime.datetime):
            representation = obj.isoformat()
            if representation.endswith('+00:00'):
                representation = representation[:-6] + 'Z'
            return representation
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            representation = obj.isoformat()
            if obj.microsecond:
                representation = representation[:12]
            return representation
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif hasattr(obj, '__getitem__'):
            try:
                return dict(obj)
            except:
                pass
        elif hasattr(obj, '__iter__'):
            return tuple(item for item in obj)
        return super(JSONEncoder, self).default(obj)
