# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The collection_contents lookup plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
    name: collection_contents
    author: Bradley Thornton (@cidrblock)
    version_added: "2.11.0"
    short_description: Retrieve the contents of a file within an ansible collection
    description:
      - Provided a dot delimited path to a file within an ansible collection, return the contents of that file.
    options:
      path:
        description:
          - The dot delimited path to the file within an ansible collection.
        type: str

    notes:
"""

EXAMPLES = r"""
- name: Retrieve the contents of a yaml file within a collection
  ansible.builtin.set_fact:
    contents: "{{ lookup('ansible.utils.collection_contents', path=path) | from_yaml }}"
  vars:
    path: ansible.utils.meta.runtime.yml

# TASK [Retrieve the contents of a yaml file within a collection] *********************
#     task path: /home/bthornto/github/ansible.utils/site.yaml:15
#     ok: [localhost] => {
#         "ansible_facts": {
#             "contents": {
#                 "requires_ansible": ">=2.9.10"
#             }
#         },
#         "changed": false
#     }

- name: Retrieve the contents of a test file within a collection
  ansible.builtin.set_fact:
    contents: "{{ lookup('ansible.utils.collection_contents', path=path) | from_yaml }}"
  vars:
    path: ansible.utils.tests.integration.targets.utils_collection_contents.vars.main.yaml

# TASK [Retrieve the contents of a test file within a collection] *********************
# task path: /home/bthornto/github/ansible.utils/site.yaml:26
# ok: [localhost] => {
#     "ansible_facts": {
#         "contents": {
#             "test_variable": 42
#         }
#     },
#     "changed": false
# }
"""

RETURN = """
  _raw:
    description:
      - The contents of the file.
"""
import sys

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible import __version__ as ansible_version_str


# Up to python 3.11 and ansible 2.14 importlib.resources fails
# this includes later version of importlib_resources
# so, the version of importlib_resources is pinned to < 5.0
# which is 3.9 like functionality
if sys.version_info >= (3, 9):
    from importlib.resources import files
from importlib_resources import read_text


class LookupModule(LookupBase):
    """The collection_contents lookup plugin."""

    def run(self, terms, variables=None, **kwargs):
        """Retrieve the contents of a file within an ansible collection.

        Args:
            terms (list): The terms passed to the lookup plugin.
            variables (dict): The variables available to the lookup plugin.
            **kwargs: Additional keyword arguments passed to the lookup plugin.
        Returns:
            The contents of the file.
        """
        # pylint: disable=unused-argument
        # pylint: disable=too-many-locals
        if isinstance(terms, list):
            keys = ["path"]
            terms = dict(zip(keys, terms))
        terms.update(kwargs)

        schema = [v for k, v in globals().items() if k.lower() == "documentation"]
        aav = AnsibleArgSpecValidator(data=terms, schema=schema[0], name="collection_contents")
        valid, errors, updated_data = aav.validate()
        if not valid:
            raise AnsibleLookupError(errors)

        path = updated_data["path"]
        parts = path.rsplit(".", 2)
        if len(parts) != 3:
            raise AnsibleLookupError(f"Malformed path: {path}")

        full_package = f"ansible_collections.{parts[0]}"
        filename = ".".join(parts[1:])
        major, minor, _ = ansible_version_str.split(".", 2)
        ansible_version = (int(major), int(minor))
        try:
            if sys.version_info >= (3, 11) and ansible_version >= (2, 15):
                with files(full_package).joinpath(filename).open("r", encoding="utf-8") as fhand:
                    content = fhand.read()
            else:
                content = read_text(full_package, filename)  # pylint:disable=used-before-assignment
        except FileNotFoundError as exc:
            raise AnsibleLookupError(f"File not found: {path} {exc}") from exc
        except ModuleNotFoundError as exc:
            raise AnsibleLookupError(f"Collection not found: {parts[0]}") from exc

        return [content]
