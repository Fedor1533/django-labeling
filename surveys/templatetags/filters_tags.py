from django import template
from django.core.files.storage import default_storage
from ..models import *

from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def define(val=None):
    """define variable with value"""
    return val

@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)

@register.filter
def is_in_survey(sources, survey):
    """add filter option in template"""
    try:
        source = sources.get(survey=survey)
    except Source.DoesNotExist:
        source = None
    return source

@register.filter
def file_exists(filepath):
    full_path = os.path.join(settings.BASE_DIR, 'static', filepath)
    if os.path.isfile(full_path):
        return filepath
    else:
        new_filepath = 'images/file_not_found.pdf' if filepath[-3:] == 'pdf' else 'images/file_not_found.png'
        return new_filepath
