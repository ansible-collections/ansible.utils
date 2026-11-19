.. _ansible.utils.reduce_on_networks_filter:


********************************
ansible.utils.reduce_on_networks
********************************

**This filter reduces a list of addresses to only the addresses that match any of the given networks.**


Version added: 6.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter reduces a list of addresses to only the addresses that match any of the given networks.
- To check whether multiple addresses belong to any of the networks, use the reduce_on_networks filter.
- To check which of the IP address of a host can be used to talk to another host, use the reduce_on_networks filter.




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
                    <b>networks</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The networks to validate against.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>the list of addresses to filter on.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: To check whether multiple addresses belong to any of the networks, use the reduce_on_networks filter.
      debug:
        msg: "{{ ['192.168.0.34', '10.3.0.3', '192.168.2.34'] | ansible.utils.reduce_on_networks( ['192.168.0.0/24', '192.128.0.0/9', '127.0.0.1/8'] ) }}"

    # TASK [To check whether multiple addresses belong to any of the networks, use the reduce_on_networks filter.] ***********
    # task path: /Users/amhatre/ansible-collections/playbooks/test_reduce_on_network.yaml:7
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": {
    #         "192.168.0.34": [
    #             "192.168.0.0/24",
    #             "192.128.0.0/9"
    #         ],
    #         "192.168.2.34": [
    #             "192.128.0.0/9"
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
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>Returns the filtered addresses belonging to any of the networks. The dict&#x27;s key is the address, the value is a list of the matching networks</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jonny007-MKD


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
