"""The pytest conftest.py file is used to setup the collection for testing."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

import yaml

try:
    from ansible.utils.collection_loader._collection_finder import (
        _AnsibleCollectionFinder,
    )

    HAS_COLLECTION_FINDER = True
except ImportError:
    HAS_COLLECTION_FINDER = False


def get_collection_name():
    """Get the collection namespace and name from the galaxy.yml file."""
    info_file = "galaxy.yml"

    try:
        with open(info_file, "r", encoding="utf-8") as fh:
            galaxy_info = yaml.safe_load(fh)
    except FileNotFoundError:
        return None, None

    return galaxy_info["namespace"], galaxy_info["name"]


def pytest_sessionstart(session):
    """Prepare for a test session.

    In the case of > 2.9, initialize the collection finder with the collection path
    otherwise, inject the collection path into sys.path.

    """
    # pylint: disable=unused-argument

    namespace, name = get_collection_name()
    if namespace is None or name is None:
        # Tests may not being run from the root of the repo.
        return

    parent_directory = os.path.dirname(os.path.dirname(__file__))
    collections_dir = os.path.join(parent_directory, "collections")
    name_dir = os.path.join(
        collections_dir, "ansible_collections", namespace, name
    )

    # If it's here, we will trust it was from this
    if not os.path.isdir(name_dir):
        os.makedirs(name_dir, exist_ok=True)

        for entry in os.listdir(parent_directory):
            if entry == "collections":
                continue
            os.symlink(os.path.abspath(entry), os.path.join(name_dir, entry))

    if HAS_COLLECTION_FINDER:
        # pylint: disable=protected-access
        _AnsibleCollectionFinder(paths=collections_dir)._install()
    else:
        sys.path.insert(0, collections_dir)
