# -*- encoding: utf-8 -*-

from jinja2.utils import soft_unicode


def map_format(value, pattern):
    """
    Apply python string formatting on an object:
    .. sourcecode:: jinja
        {{ "%s - %s"|format("Hello?", "Foo!") }}
            -> Hello? - Foo!
    e.g.  
    "{{ groups['meta']|map('map_format', '%s:9559')|join(',') }}"
    """
    return soft_unicode(pattern) % (value)


class FilterModule(object):
    """ jinja2 filters """

    def filters(self):
        return {
            'map_format': map_format,
        }