.. _ansible.utils.replace_keys_filter:


**************************
ansible.utils.replace_keys
**************************

**Replaces specific keys with their after value from a data recursively.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin replaces specific keys with their after value from a data recursively.
- Matching parameter defaults to equals unless ``matching_parameter`` is explicitly mentioned.
- Using the parameters below- ``data|ansible.utils.replace_keys(target([....]``))




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This option represents a list of dictionaries or a dictionary with any level of nesting data.</div>
                        <div>For example <code>config_data|ansible.utils.replace_keys(target([....]</code>)), in this case <code>config_data</code> represents this option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>matching_parameter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>starts_with</li>
                                    <li>ends_with</li>
                                    <li>regex</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the matching configuration of target keys and data attributes.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the target keys to replace in list of dictionaries format containing before and after key value.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>after</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>after attribute key [change to]</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>before</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>before attribute key [to change]</div>
                </td>
            </tr>

    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    ##example.yaml
    interfaces:
      - interface_name: eth0
        enabled: true
        duplex: auto
        speed: auto
      - interface_name: eth1
        description: Configured by Ansible - Interface 1
        mtu: 1500
        speed: auto
        duplex: auto
        is_enabled: true
        vifs:
        - vlan_id: 100
          description: Eth1 - VIF 100
          mtu: 400
          is_enabled: true
        - vlan_id: 101
          description: Eth1 - VIF 101
          is_enabled: true
      - interface_name: eth2
        description: Configured by Ansible - Interface 2 (ADMIN DOWN)
        mtu: 600
        is_enabled: false

    ##Playbook
    vars_files:
      - "example.yaml"
    tasks:
      - name: replace keys with specified keys dict/list to dict
        ansible.builtin.set_fact:
          data: "{{ interfaces }}"

      - debug:
          msg:  "{{ data|ansible.utils.replace_keys(target=[{'before':'interface_name', 'after':'name'}, {'before':'is_enabled', 'after':'enabled'}]) }}"

    ##Output
    # TASK [replace keys with specified keys dict/list to dict] *************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "data": [
    #             {
    #                 "duplex": "auto",
    #                 "enabled": true,
    #                 "interface_name": "eth0",
    #                 "speed": "auto"
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 1",
    #                 "duplex": "auto",
    #                 "interface_name": "eth1",
    #                 "is_enabled": true,
    #                 "mtu": 1500,
    #                 "speed": "auto",
    #                 "vifs": [
    #                     {
    #                         "description": "Eth1 - VIF 100",
    #                         "is_enabled": true,
    #                         "mtu": 400,
    #                         "vlan_id": 100
    #                     },
    #                     {
    #                         "description": "Eth1 - VIF 101",
    #                         "is_enabled": true,
    #                         "vlan_id": 101
    #                     }
    #                 ]
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #                 "interface_name": "eth2",
    #                 "is_enabled": false,
    #                 "mtu": 600
    #             }
    #         ]
    #     },
    #     "changed": false
    # }

    # TASK [debug] **********************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         {
    #             "duplex": "auto",
    #             "enabled": true,
    #             "name": "eth0",
    #             "speed": "auto"
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 1",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth1",
    #             "speed": "auto",
    #             "vifs": [
    #                 {
    #                     "description": "Eth1 - VIF 100",
    #                     "enabled": true,
    #                     "mtu": 400,
    #                     "vlan_id": 100
    #                 },
    #                 {
    #                     "description": "Eth1 - VIF 101",
    #                     "enabled": true,
    #                     "vlan_id": 101
    #                 }
    #             ]
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #             "enabled": false,
    #             "mtu": 600,
    #             "name": "eth2"
    #         }
    #     ]
    # }

    ##example.yaml
    interfaces:
      - interface_name: eth0
        enabled: true
        duplex: auto
        speed: auto
      - interface_name: eth1
        description: Configured by Ansible - Interface 1
        mtu: 1500
        speed: auto
        duplex: auto
        is_enabled: true
        vifs:
        - vlan_id: 100
          description: Eth1 - VIF 100
          mtu: 400
          is_enabled: true
        - vlan_id: 101
          description: Eth1 - VIF 101
          is_enabled: true
      - interface_name: eth2
        description: Configured by Ansible - Interface 2 (ADMIN DOWN)
        mtu: 600
        is_enabled: false

    ##Playbook
    vars_files:
      - "example.yaml"
    tasks:
      - name: replace keys with specified keys dict/list to dict
        ansible.builtin.set_fact:
          data: "{{ interfaces }}"

      - debug:
          msg:  "{{ data|ansible.utils.replace_keys(target=[{'before':'name', 'after':'name'}, {'before':'enabled', 'after':'enabled'}],
                matching_parameter= 'ends_with') }}"

    ##Output
    # TASK [replace keys with specified keys dict/list to dict] *********************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "data": [
    #             {
    #                 "duplex": "auto",
    #                 "enabled": true,
    #                 "interface_name": "eth0",
    #                 "speed": "auto"
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 1",
    #                 "duplex": "auto",
    #                 "interface_name": "eth1",
    #                 "is_enabled": true,
    #                 "mtu": 1500,
    #                 "speed": "auto",
    #                 "vifs": [
    #                     {
    #                         "description": "Eth1 - VIF 100",
    #                         "is_enabled": true,
    #                         "mtu": 400,
    #                         "vlan_id": 100
    #                     },
    #                     {
    #                         "description": "Eth1 - VIF 101",
    #                         "is_enabled": true,
    #                         "vlan_id": 101
    #                     }
    #                 ]
    #             },
    #             {
    #                 "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #                 "interface_name": "eth2",
    #                 "is_enabled": false,
    #                 "mtu": 600
    #             }
    #         ]
    #     },
    #     "changed": false
    # }

    # TASK [debug] ***************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         {
    #             "duplex": "auto",
    #             "enabled": true,
    #             "name": "eth0",
    #             "speed": "auto"
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 1",
    #             "duplex": "auto",
    #             "enabled": true,
    #             "mtu": 1500,
    #             "name": "eth1",
    #             "speed": "auto",
    #             "vifs": [
    #                 {
    #                     "description": "Eth1 - VIF 100",
    #                     "enabled": true,
    #                     "mtu": 400,
    #                     "vlan_id": 100
    #                 },
    #                 {
    #                     "description": "Eth1 - VIF 101",
    #                     "enabled": true,
    #                     "vlan_id": 101
    #                 }
    #             ]
    #         },
    #         {
    #             "description": "Configured by Ansible - Interface 2 (ADMIN DOWN)",
    #             "enabled": false,
    #             "mtu": 600,
    #             "name": "eth2"
    #         }
    #     ]
    # }




Status
------


Authors
~~~~~~~

- Sagar Paul (@KB-perByte)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
