# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The get_path lookup plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
    lookup: get_path
    author: Bradley Thornton (@cidrblock)
    version_added: "1.0"
    short_description: Retrieve the value in a variable using a path
    description:
        - Use a C(path) to retreive a nested value from a C(var)
        - C(get_path) is also available as a C(filter_plugin) for convenience
    options:
      var:
        description: The variable from which the value should be extraced
        type: raw
        required: True
      path:
        description: >
            The C(path) in the C(var) to retrieve the value of.
            The C(path) needs to a be a valid jinja path
        type: str
        required: True
      wantlist:
        description: >
            If set to C(True), the return value will always be a list
            This can also be accomplished using C(query) or C(q) instead of C(lookup)
            U(https://docs.ansible.com/ansible/latest/plugins/lookup.html)
        type: bool

    notes:
"""

EXAMPLES = r"""
- ansible.builtin.set_fact:
    a:
      b:
        c:
          d:
          - 0
          - 1
          e:
          - True
          - False

- name: Retrieve a value deep inside a using a path
  ansible.builtin.set_fact:
    as_lookup: "{{ lookup('ansible.utils.get_path', a, path) }}"
    as_filter: "{{ a|ansible.utils.get_path(path) }}"
  vars:
    path: b.c.d[0]

# TASK [ansible.builtin.set_fact] *************************************
# ok: [nxos101] => changed=false
#   ansible_facts:
#     as_filter: '0'
#     as_lookup: '0'


#### Working with hostvars

- name: Retrieve a value deep inside all of the host's vars
  ansible.builtin.set_fact:
    as_lookup: "{{ lookup('ansible.utils.get_path', look_in, look_for) }}"
    as_filter: "{{ look_in|ansible.utils.get_path(look_for) }}"
  vars:
    look_in: "{{ hostvars[inventory_hostname] }}"
    look_for: a.b.c.d[0]

# TASK [Retrieve a value deep inside all of the host's vars] **********
# ok: [nxos101] => changed=false
#   ansible_facts:
#     as_filter: '0'
#     as_lookup: '0'


#### Used alongside ansible.utils.to_paths

- name: Get the paths for the object
  ansible.builtin.set_fact:
    paths: "{{ a|ansible.utils.to_paths(prepend='a') }}"

- name: Retrieve the value of each path from vars
  ansible.builtin.debug:
    msg: "The value of path {{ path }} in vars is {{ value }}"
  loop: "{{ paths.keys()|list }}"
  loop_control:
    label: "{{ item }}"
  vars:
    path: "{{ item }}"
    value: "{{ vars|ansible.utils.get_path(item) }}"

# TASK [Get the paths for the object] *********************************
# ok: [nxos101] => changed=false
#   ansible_facts:
#     paths:
#       a.b.c.d[0]: 0
#       a.b.c.d[1]: 1
#       a.b.c.e[0]: true
#       a.b.c.e[1]: false

# TASK [Retrieve the value of each path from vars] ********************
# ok: [nxos101] => (item=a.b.c.d[0]) =>
#   msg: The value of path a.b.c.d[0] in vars is 0
# ok: [nxos101] => (item=a.b.c.d[1]) =>
#   msg: The value of path a.b.c.d[1] in vars is 1
# ok: [nxos101] => (item=a.b.c.e[0]) =>
#   msg: The value of path a.b.c.e[0] in vars is True
# ok: [nxos101] => (item=a.b.c.e[1]) =>
#   msg: The value of path a.b.c.e[1] in vars is False


#### Working with complex structures

- name: Retrieve the current interface config
  cisco.nxos.nxos_interfaces:
    state: gathered
  register: interfaces

- name: Get the description of several interfaces
  ansible.builtin.debug:
    msg: "{{ rekeyed|ansible.utils.get_path(item) }}"
  vars:
    rekeyed:
      by_name: "{{ interfaces.gathered|ansible.builtin.rekey_on_member('name') }}"
  loop:
  - by_name['Ethernet1/1'].description
  - by_name['Ethernet1/2'].description

# TASK [Get the description of several interfaces] ********************
# ok: [nxos101] => (item=by_name['Ethernet1/1'].description) =>
#   msg: Configured by Ansible
# ok: [nxos101] => (item=by_name['Ethernet1/2'].description) =>
#   msg: Configured by Ansible Network

"""

RETURN = """
  _raw:
    description:
      - One or more zero-based indicies of the matching list items
      - See C(wantlist) if a list is always required
"""

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from ansible_collections.ansible.utils.plugins.module_utils.common.get_path import (
    get_path,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        if isinstance(terms, list):
            keys = ["var", "path"]
            terms = dict(zip(keys, terms))
        terms.update(kwargs)
        aav = AnsibleArgSpecValidator(
            data=terms,
            schema=DOCUMENTATION,
            name="get_path",
        )
        valid, errors, updated_data = aav.validate()
        if not valid:
            raise AnsibleLookupError(errors)
        updated_data["wantlist"] = True
        updated_data["environment"] = self._templar.environment
        res = get_path(**updated_data)
        return res
