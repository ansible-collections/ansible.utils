# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: fact_diff
short_description: Find the difference between currently set facts
version_added: "1.0.0"
description:
    - Compare two facts or variables and get a diff
options:
  before:
    description:
      - The first fact to be used in the comparison
    type: raw
    required: True
  after:
    description:
      - The second fact to be used in the comparison
    type: raw
    required: True  

notes:

author:
- Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""

  - set_fact:
      left:
        a:
          b:
            c:
              d:
              - 0
              - 1
      right:
        a:
          b:
            c:
              d:
              - 2
              - 3

- name: Show the difference in json format
  ansible.utils.fact_diff:
    before: "{{ left }}"
    after: "{{ right }}"

# TASK [ansible.utils.fact_diff] **************************************
# --- before
# +++ after
# @@ -3,8 +3,8 @@
#          "b": {
#              "c": {
#                  "d": [
# -                    0,
# -                    1
# +                    2,
# +                    3
#                  ]
#              }
#          }
#
# changed: [localhost]

- name: Show the difference in path format
  ansible.utils.fact_diff:
    before: "{{ left|ansible.utils.to_paths }}"
    after: "{{ right|ansible.utils.to_paths }}"

# TASK [ansible.utils.fact_diff] **************************************
# --- before
# +++ after
# @@ -1,4 +1,4 @@
#  {
# -    "a.b.c.d[0]": 0,
# -    "a.b.c.d[1]": 1
# +    "a.b.c.d[0]": 2,
# +    "a.b.c.d[1]": 3
#  }
#
# changed: [localhost]

- name: Show the difference in yaml format
  ansible.utils.fact_diff:
    before: "{{ left|to_nice_yaml }}"
    after: "{{ right|to_nice_yaml }}"

# TASK [ansible.utils.fact_diff] **************************************
# --- before
# +++ after
# @@ -2,5 +2,5 @@
#      b:
#          c:
#              d:
# -            - 0
# -            - 1
# +            - 2
# +            - 3

# changed: [localhost]


"""
