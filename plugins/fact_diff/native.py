# -*- coding: utf-8 -*-
# Copyafter 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from ansible.plugins.callback import CallbackBase
from ansible_collections.ansible.utils.plugins.module_utils.base_classes.fact_diff import (
    FactDiffBase,
)


class FactDiff(FactDiffBase):
    def _check_valid_regexes(self):
        if self._skip_lines:
            self.debug("Checking regex in 'split_lines' for validity")
            for idx, regex in enumerate(self._skip_lines):
                try:
                    self._skip_lines[idx] = re.compile(regex)
                except re.error as exc:
                    msg = "The regex '{regex}', is not valid. The error was {err}.".format(
                        regex=regex, err=str(exc)
                    )
                    self._errors.append(msg)

    def _xform(self):
        if self._skip_lines:
            if isinstance(self._before, str):
                self._debug("'before' is a string, splitting lines")
                self._before = self._before.splitlines()
            if isinstance(self._after, str):
                self._debug("'after' is a string, splitting lines")
                self._after = self._after.splitlines()
            self._before = [
                l
                for l in self._before
                if not any(regex.match(str(l)) for regex in self._skip_lines)
            ]
            self._after = [
                l
                for l in self._after
                if not any(regex.match(str(l)) for regex in self._skip_lines)
            ]
        if isinstance(self._before, list):
            self._debug("'before' is a list, joining with \n")
            self._before = "\n".join(map(str, self._before)) + "\n"
        if isinstance(self._after, list):
            self._debug("'after' is a list, joining with \n")
            self._after = "\n".join(map(str, self._after)) + "\n"

    def diff(self):
        self._after = self._task_args["after"]
        self._before = self._task_args["before"]
        self._errors = []
        self._skip_lines = self._task_args["plugin"]["vars"].get("skip_lines")
        self._check_valid_regexes()
        if self._errors:
            return {"errors": " ".join(self._errors)}
        self._xform()
        diff = CallbackBase()._get_diff(
            {"before": self._before, "after": self._after}
        )
        return {"diff": diff}
