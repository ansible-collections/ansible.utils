.. _ansible.utils.param_list_compare_filter:


********************************
ansible.utils.param_list_compare
********************************

**Generate the final param list combining/comparing base and provided parameters.**


Version added: 2.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Generate the final list of parameters after comparing with base list and provided/target list of params/bangs.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>base</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the base list.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Specify the target list.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - set_fact:
        base: ['1', '2', '3', '4', ' 5']

    - set_fact:
        target: ['!all', '2', '4']

    - name: Get final list of parameters
      register: result
      set_fact:
        final_params: "{{ base | param_list_compare(target) }}"

    # TASK [Target list] **********************************************************
    # ok: [localhost] => {
    #     "msg": {
    #         "actionable": [
    #             "2",
    #             "4"
    #         ],
    #         "unsupported": []
    #     }
    # }

    - set_fact:
        base: ['1', '2', '3', '4', '5']

    - name: Get final list of parameters
      register: result
      set_fact:
        final_params: "{{ base|param_list_compare(target=['2', '7', '8']) }}"

    # TASK [Get final list of parameters] ********************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "final_params": {
    #             "actionable": [
    #                 "2"
    #             ],
    #             "unsupported": [
    #                 "7",
    #                 "8"
    #             ]
    #         }
    #     },
    #     "changed": false
    # }

    # Network Specific Example
    # -----------
    - set_fact:
        ios_resources:
          - "acl_interfaces"
          - "acls"
          - "bgp_address_family"
          - "bgp_global"
          - "interfaces"
          - "l2_interfaces"
          - "l3_interfaces"
          - "lacp"
          - "lacp_interfaces"
          - "lag_interfaces"
          - "lldp_global"
          - "lldp_interfaces"
          - "logging_global"
          - "ospf_interfaces"
          - "ospfv2"
          - "ospfv3"
          - "prefix_lists"
          - "route_maps"
          - "static_routes"
          - "vlans"

    - set_fact:
        target_resources:
          - '!all'
          - 'vlan'
          - 'bgp_global'

    - name: Get final list of target resources/params
      register: result
      set_fact:
        network_resources: "{{ ios_resources|param_list_compare(target_resources) }}"

    - name: Target list of network resources
      debug:
        msg: "{{ network_resources }}"

    # TASK [Target list of network resources] *******************************************************************************************************************
    # ok: [localhost] => {
    #     "msg": {
    #         "actionable": [
    #             "bgp_global",
    #             "vlans"
    #         ],
    #         "unsupported": []
    #     }
    # }

    - name: Get final list of target resources/params
      register: result
      set_fact:
        network_resources: "{{ ios_resources|param_list_compare(target=['vla', 'ntp_global', 'logging_global']) }}"

    - name: Target list of network resources
      debug:
        msg: "{{ network_resources }}"

    # TASK [Target list of network resources] ************************************************
    # ok: [localhost] => {
    #     "msg": {
    #         "actionable": [
    #             "logging_global"
    #         ],
    #         "unsupported": [
    #             "vla",
    #             "ntp_global"
    #         ]
    #     }
    # }



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this filter:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>actionable</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>list of combined params</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>unsupported</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>list of unsupported params</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
