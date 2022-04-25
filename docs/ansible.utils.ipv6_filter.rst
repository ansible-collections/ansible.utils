.. _ansible.utils.ipv6_filter:


******************
ansible.utils.ipv6
******************

**To filter only Ipv6 addresses Ipv6 filter is used.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Sometimes you need only IPv6 addresses. To filter only Ipv6 addresses Ipv6 filter is used.




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
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>You can provide a single argument to each ipv6() filter.</div>
                        <div>Example. query type &#x27;ipv4&#x27; to convert ipv6 into ipv4</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
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
                        <div>list of subnets or individual address or any other values input for ipv6 plugin</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    # Ipv6 filter plugin with different queries.
    - name: Set value as input list
      ansible.builtin.set_fact:
           value:
                - 192.24.2.1
                - ::ffff:192.168.32.0/120
                - ''
                - ::ffff:192.24.2.1/128
                - 192.168.32.0/24
                - fe80::100/10
                - True
    - name: IPv6 filter to filter Ipv6 Address
      debug:
        msg: "{{ value|ansible.utils.ipv6 }}"

    - name: convert IPv6 addresses into IPv4 addresses.
      debug:
        msg: "{{ value|ansible.utils.ipv6('ipv4') }}"

    - name: filter only  IPv6 addresses.
      debug:
        msg: "{{ value|ansible.utils.ipv6('address') }}"


    # PLAY [Ipv6 filter plugin with different queries.] ******************************************************************
    # TASK [Set value as input list] ***************************************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "value": [
    #             "192.24.2.1",
    #             "::ffff:192.168.32.0/120",
    #             "",
    #             "::ffff:192.24.2.1/128",
    #             "192.168.32.0/24",
    #             "fe80::100/10",
    #             true
    #         ]
    #     },
    #     "changed": false
    # }
    #
    # TASK [IPv6 filter to filter Ipv6 Address] ****************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "::ffff:192.168.32.0/120",
    #         "::ffff:192.24.2.1/128",
    #         "fe80::100/10"
    #     ]
    # }
    #
    # TASK [convert IPv6 addresses into IPv4 addresses.] *******************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.168.32.0/24",
    #         "192.24.2.1/32"
    #     ]
    # }
    #
    # TASK [filter only  IPv6 addresses] *******************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "::ffff:192.168.32.0",
    #         "::ffff:192.24.2.1",
    #         "fe80::100"
    #     ]
    # }
    #



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
                      <span style="color: purple">raw</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>Returns values valid for a particular query.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ashwini Mhatre (@amhatre)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
