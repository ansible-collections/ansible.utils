# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit test file for ipwrap filter plugin."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.utils.plugins.filter.next_nth_usable import _next_nth_usable


class Test_Next_Nth_Usable(unittest.TestCase):
    def setUp(self):
        pass

    def test_next_nth_usable_filter(self):
        """next_nth_usable filter."""
        args = ["", "192.168.122.1/24", 2]
        result = _next_nth_usable(*args)
        assert result == "192.168.122.3"

    def test_next_nth_usable_with_empty_return_string(self):
        """Check ipv4 to ipv6 conversion."""
        args = ["", "192.168.122.254/24", 2]
        result = _next_nth_usable(*args)
        assert result is None
