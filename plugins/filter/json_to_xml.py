# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: json_to_xml
    author: Ashwini Mhatre (@amhatre)
    version_added: "1.0.0"
    short_description: convert given json string to xml
    description:
        - This plugin converts the xml string to json.
        - Using the parameters below- C(data|ansible.utils.json_to_xml)
    options:
      data:
        description:
        - The input json string .
        - This option represents the json value that is passed to the filter plugin in pipe format.
        - For example C(config_data|ansible.utils.json_to_xml), in this case C(config_data) represents this option.
        type: str
        required: True
"""

EXAMPLES = r"""

#### Simple examples

- name: Define json data 
    ansible.builtin.set_fact:
      data: {
        "interface-configurations": {
          "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
          "interface-configuration": null
        }
      }
  - debug:
      msg:  "{{ data|ansible.utils.json_to_xml }}"

TASK [Define json data ] *************************************************************************
task path: /Users/amhatre/ansible-collections/playbooks/test_utils_json_to_xml.yaml:5
ok: [localhost] => {
    "ansible_facts": {
        "data": {
            "interface-configurations": {
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg",
                "interface-configuration": null
            }
        }
    },
    "changed": false
}

TASK [debug] ***********************************************************************************************************
task path: /Users/amhatre/ansible-collections/playbooks/test_utils_json_to_xml.yaml:13
Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
ok: [localhost] => {
    "msg": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<interface-configurations xmlns=\"http://cisco.com/ns/yang/
    Cisco-IOS-XR-ifmgr-cfg\">\n\t<interface-configuration></interface-configuration>\n</interface-configurations>"
}



"""

from ansible.errors import AnsibleFilterError
from jinja2.filters import environmentfilter
from ansible_collections.ansible.utils.plugins.module_utils.common.json_to_xml import (
    json_to_xml,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)


@environmentfilter
def _json_to_xml(*args, **kwargs):
    """Convert the given data from xml to json."""

    keys = [
        "environment",
        "data",
    ]
    data = dict(zip(keys, args))
    data.update(kwargs)
    environment = data.pop("environment")
    aav = AnsibleArgSpecValidator(
        data=data, schema=DOCUMENTATION, name="json_to_xml"
    )
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    updated_data["tests"] = environment.tests
    return json_to_xml(**updated_data)


class FilterModule(object):
    """ json_to_xml  """

    def filters(self):
        """a mapping of filter names to functions"""
        return {"json_to_xml": _json_to_xml}