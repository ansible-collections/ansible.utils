# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit test file for netaddr test plugin: ip."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.utils.plugins.test.ip import _ip


class TestIp(unittest.TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec."""
        # missing argument
        with self.assertRaises(TypeError) as error:
            _ip()
        assert "argument" in str(error.exception)

    def test_valid_data(self):
        """Check passing valid data as per criteria."""
        result = _ip(ip="10.1.1.1")
        assert result is True

        result = _ip(ip="2001:db8:a::123")
        assert result is True

        result = _ip(ip="string")
        assert result is False

        result = _ip(ip="300.1.1.1")
        assert result is False

        result = _ip(ip="10.0.0.0/8")
        assert result is True
