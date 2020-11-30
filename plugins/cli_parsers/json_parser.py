"""
json parser

This is the json parser for use with the cli_parse module and action plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils._text import to_native
from ansible.module_utils.six import string_types
from ansible_collections.ansible.utils.plugins.cli_parsers._base import (
    CliParserBase,
)


class CliParser(CliParserBase):
    """ The json parser class
    Convert a string containing valid json into an object
    """

    DEFAULT_TEMPLATE_EXTENSION = None
    PROVIDE_TEMPLATE_CONTENTS = False

    def parse(self, *_args, **_kwargs):
        """ Std entry point for a cli_parse parse execution

        :return: Errors or parsed text as structured data
        :rtype: dict

        :example:

        The parse function of a parser should return a dict:
        {"errors": [a list of errors]}
        or
        {"parsed": obj}
        """
        text = self._task_args.get("text")
        try:
            if not isinstance(text, string_types):
                text = json.dumps(text)
            parsed = json.loads(text)
        except Exception as exc:
            return {"errors": [to_native(exc)]}

        return {"parsed": parsed}
