# -*- coding: utf-8 -*-
# Copyafter 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
import re
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail
from ansible.plugins.callback import CallbackBase
from ansible_collections.ansible.utils.plugins.modules.fact_diff import (
    DOCUMENTATION,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)



class ActionModule(ActionBase):
    """ action module
    """

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._before = None
        self._after = None
        self._result = None

    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=DOCUMENTATION,
            schema_format="doc",
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)

    def _set_vars(self):
        self._before = self._task.args.get('before')
        if isinstance(self._before, list):
            self._before = {'before': self._before}
        self._after = self._task.args.get('after')
        if isinstance(self._after, list):
            self._after = {'after': self._after}
     
    def run(self, tmp=None, task_vars=None):
        self._task.diff = True
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._check_argspec()
        self._set_vars()
        diff_dict = {'before': self._before, 'after': self._after}

        diff_text = CallbackBase()._get_diff(diff_dict)
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        diff_text = ansi_escape.sub('', diff_text)

        self._result.update({
            'diff': diff_dict,
            'changed': bool(diff_text),
            'diff_lines': diff_text.splitlines(),
            'diff_text': diff_text
        })
        return self._result