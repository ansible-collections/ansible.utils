from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest


try:
    from pytest_ansible_network_integration.defs import LocalhostProject  # noqa: F401

    HAS_PLUGIN = True
except ImportError:
    HAS_PLUGIN = False


if not HAS_PLUGIN:

    @pytest.fixture
    def localhost_project():
        pytest.skip("pytest-ansible-network-integration is not installed")

    @pytest.fixture
    def environment():
        pytest.skip("pytest-ansible-network-integration is not installed")
