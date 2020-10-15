# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The action plugin file for cli_parse
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils._text import to_bytes
from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible.module_utils import basic

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec import generate_argspec


class ActionModule(ActionBase):
    """ action module
    """
    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._playhost = None

        self._result = {}
        self._task_vars = None

    def _debug(self, name, msg):
        """ Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "<{phost}> {name} {msg}".format(
            phost=self._playhost, name=name, msg=msg
        )
        self._display.vvvv(msg)

    def _fail_json(self, msg):
        """ Replace the AnsibleModule fai_json here

        :param msg: The message for the failure
        :type msg: str
        """
        msg = msg.replace("(basic.py)", self._task.action)
        raise AnsibleActionFail(msg)

    def _check_argspec(self, docs, conditionals={}):
        """ Load the doc and convert
        Add the root conditionals to what was returned from the conversion
        and instantiate an AnsibleModule to validate
        """
        argspec = generate_argspec(docs, conditionals=conditionals)
        basic._ANSIBLE_ARGS = to_bytes(
            json.dumps({"ANSIBLE_MODULE_ARGS": self._task.args})
        )
        basic.AnsibleModule.fail_json = self._fail_json
        basic.AnsibleModule(**argspec)

    def _extended_check_argspec(self):
        """ Check additional requirements for the argspec
        that cannot be covered using stnd techniques
        """
        pass
