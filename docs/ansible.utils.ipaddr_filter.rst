.. _ansible.utils.ipaddr_filter:


********************
ansible.utils.ipaddr
********************

**This filter is designed to return the input value if a query is True, else False.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter is designed to return the input value if a query is True, and False if a query is False
- This way it can be easily used in chained filters




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
                    <b>alias</b>
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
                        <div>type of filter. example ipaddr, ipv4, ipv6, ipwrap</div>
                </td>
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
                        <div>You can provide a single argument to each ipaddr() filter.</div>
                        <div>The filter will then treat it as a query and return values modified by that query.</div>
                        <div>Types of queries include: 1. query by name: ansible.utils.ipaddr(&#x27;address&#x27;), ansible.utils.ipv4(&#x27;network&#x27;); 2. query by CIDR range: ansible.utils.ipaddr(&#x27;192.168.0.0/24&#x27;), ansible.utils.ipv6(&#x27;2001:db8::/32&#x27;); 3. query by index number: ansible.utils.ipaddr(&#x27;1&#x27;), ansible.utils.ipaddr(&#x27;-1&#x27;);</div>
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
                        <div>list of subnets or individual address or any other values input for ipaddr plugin</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Ip version 4 or 6</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    # Ipaddr filter plugin with different queries.
    - name: Set value as input list
      ansible.builtin.set_fact:
        value:
          - 192.24.2.1
          - host.fqdn
          - ::1
          - ''
          - 192.168.32.0/24
          - fe80::100/10
          - 42540766412265424405338506004571095040/64
          - True
    - debug:
        msg: "{{ value|ansible.utils.ipaddr }}"

    - name: Fetch only those elements that are host IP addresses and not network ranges
      debug:
        msg: "{{ value|ansible.utils.ipaddr('address') }}"

    - name: |
        Fetch only host IP addresses with their correct CIDR prefixes (as is common with IPv6 addressing), you can use
        the ipaddr('host') filter.
      debug:
        msg: "{{ value|ansible.utils.ipaddr('host') }}"

    - name: check if IP addresses or network ranges are accessible on a public Internet and return it.
      debug:
        msg: "{{ value|ansible.utils.ipaddr('public') }}"

    - name: check if IP addresses or network ranges are accessible on a private Internet and return it.
      debug:
         msg: "{{ value|ansible.utils.ipaddr('private') }}"

    - name: check which values are values are specifically network ranges and return it.
      debug:
        msg: "{{ value|ansible.utils.ipaddr('net') }}"

    - name: check how many IP addresses can be in a certain range.
      debug:
        msg: "{{ value| ansible.utils.ipaddr('net') | ansible.utils.ipaddr('size') }}"

    - name: By specifying a network range as a query, you can check if a given value is in that range.
      debug:
        msg: "{{ value|ansible.utils.ipaddr('192.0.0.0/8') }}"

    # First IP address (network address)
    - name: |
        If you specify a positive or negative integer as a query, ipaddr() will treat this as an index and will return
        the specific IP address from a network range, in the "host/prefix" format.
      debug:
        msg: "{{ value| ansible.utils.ipaddr('net') | ansible.utils.ipaddr('0') }}"

    # Second IP address (usually the gateway host)
    - debug:
        msg: "{{ value| ansible.utils.ipaddr('net') | ansible.utils.ipaddr('1') }}"

    # Last IP address (the broadcast address in IPv4 networks)
    - debug:
        msg: "{{ value| ansible.utils.ipaddr('net') | ansible.utils.ipaddr('-1') }}"


    # PLAY [Ipaddr filter plugin with different queries.] ******************************************************************
    # TASK [Set value as input list] ***************************************************************************************
    # ok: [localhost] => {"ansible_facts": {"value": ["192.24.2.1", "host.fqdn", "::1", "", "192.168.32.0/24",
    # "fe80::100/10", "42540766412265424405338506004571095040/64", true]}, "changed": false}
    #
    # TASK [debug] ********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "::1",
    #         "192.168.32.0/24",
    #         "fe80::100/10",
    #         "2001:db8:32c:faad::/64"
    #     ]
    # }
    #
    # TASK [Fetch only those elements that are host IP addresses and not network ranges] ***********************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "::1",
    #         "fe80::100",
    #         "2001:db8:32c:faad::"
    #     ]
    # }
    #
    # TASK [Fetch only host IP addresses with their correct CIDR prefixes (as is common with IPv6 addressing), you can use
    # the ipaddr('host') filter.] *****************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1/32",
    #         "::1/128",
    #         "fe80::100/10"
    #     ]
    # }
    #
    # TASK [check if IP addresses or network ranges are accessible on a public Internet and return it.] ********************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "2001:db8:32c:faad::/64"
    #     ]
    # }
    #
    # TASK [check if IP addresses or network ranges are accessible on a private Internet and return it.] *******************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.168.32.0/24",
    #         "fe80::100/10"
    #     ]
    # }
    #
    # TASK [check which values are values are specifically network ranges and return it.] **********************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.168.32.0/24",
    #         "2001:db8:32c:faad::/64"
    #     ]
    # }
    #
    # TASK [check how many IP addresses can be in a certain range.] *********************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         256,
    #         18446744073709551616
    #     ]
    # }
    #
    # TASK [By specifying a network range as a query, you can check if a given value is in that range.] ********************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.24.2.1",
    #         "192.168.32.0/24"
    #     ]
    # }
    #
    # TASK [If you specify a positive or negative integer as a query, ipaddr() will treat this as an index and will
    # return the specific IP address from a network range, in the "host/prefix" format.] ***
    # ok: [localhost] => {
    #     "msg": [
    #         "192.168.32.0/24",
    #         "2001:db8:32c:faad::/64"
    #     ]
    # }
    #
    # TASK [debug] *********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.168.32.1/24",
    #         "2001:db8:32c:faad::1/64"
    #     ]
    # }
    #
    # TASK [debug] ********************************************************************************************************
    # ok: [localhost] => {
    #     "msg": [
    #         "192.168.32.255/24",
    #         "2001:db8:32c:faad:ffff:ffff:ffff:ffff/64"
    #     ]
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
