# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit test file for netaddr test plugin: public."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.utils.plugins.test.public import _public


class TestPublic(unittest.TestCase):
    def setUp(self):
        pass

    def test_invalid_data(self):
        """Check passing invalid argspec."""
        # missing argument
        with self.assertRaises(TypeError) as error:
            _public()
        assert "argument" in str(error.exception)

    def test_valid_data(self):
        """Check passing valid data as per criteria."""
        result = _public(ip="8.8.8.8")
        assert result is True

        result = _public(ip="10.1.1.1")
        assert result is False

        result = _public(ip="string")
        assert result is False
