.. _ansible.utils.ipsubnet_filter:


**********************
ansible.utils.ipsubnet
**********************

**This filter can be used to manipulate network subnets in several ways.**


Version added: 2.5.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This filter can be used to manipulate network subnets in several ways.




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
                    <b>index</b>
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
                        <div>The second argument of the ipsubnet() filter is an index number; by specifying it you can get a new subnet
    with the specified index.</div>
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
                        <div>You can provide query as 1st argument.
    To check if a given string is a subnet, pass it through the filter without any arguments. If the given
    string is an IP address, it will be converted into a subnet.
    If you specify a subnet size as the first parameter of the ipsubnet() filter, and the subnet size is
    smaller than the current one, you will get the number of subnets a given subnet can be split into.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>subnets or individual address or any other values input for ipsubnet plugin</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### examples
    # Ipsubnet filter plugin with different queries.
    vars:
      address: 192.168.144.5
      subnet: 192.168.0.0/16
      ipv6_address: '2001:4860:4860::8888'
      ipv6_subnet: '2600:1f1c:1b3:8f00::/56'
    tasks:
      - name: convert IP address to subnet
        debug:
          msg: '{{ address | ansible.utils.ipsubnet }}'
      - name: check if a given string is a subnet
        debug:
          msg: '{{ subnet | ansible.utils.ipsubnet }}'
      - name: Get the number of subnets a given subnet can be split into.
        debug:
          msg: '{{ subnet | ansible.utils.ipsubnet(20) }}'
      - name: Get a 1st subnet
        debug:
          msg: '{{ subnet | ansible.utils.ipsubnet(20, 0) }}'
      - name: Get a last subnet
        debug:
          msg: '{{ subnet | ansible.utils.ipsubnet(20, -1) }}'
      - name: Get first IPv6 subnet that has prefix length /120
        debug:
          msg: '{{ ipv6_subnet | ansible.utils.ipsubnet(120, 0) }}'
      - name: Get last subnet that has prefix length /120
        debug:
          msg: '{{ ipv6_subnet | ansible.utils.ipsubnet(120, -1) }}'
      - name: Get biggest subnet that contains that given IP address.
        debug:
          msg: '{{ address | ansible.utils.ipsubnet(20) }}'
      - name: Get 1st smaller subnet by specifying 0 as index number
        debug:
          msg: '{{ address | ansible.utils.ipsubnet(18, 0) }}'
      - name: Get last subnet
        debug:
          msg: '{{ address | ansible.utils.ipsubnet(18, -1) }}'
      - name: >-
          The rank of the IP in the subnet (the IP is the 36870nth /32 of the
          subnet)
        debug:
          msg: '{{ address | ansible.utils.ipsubnet(subnet) }}'
      - name: The rank in the /24 that contain the address
        debug:
          msg: '{{ address | ansible.utils.ipsubnet(''192.168.144.0/24'') }}'
      - name: An IP with the subnet in the first /30 in a /24
        debug:
          msg: '{{ ''192.168.144.1/30'' | ansible.utils.ipsubnet(''192.168.144.0/24'') }}'
      - name: The fifth subnet /30 in a /24
        debug:
          msg: '{{ ''192.168.144.16/30'' | ansible.utils.ipsubnet(''192.168.144.0/24'') }}'


    # PLAY [Ipsubnet filter plugin with different queries.] ****************************************************************
    # TASK [convert IP address to subnet] *************************************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:10
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.144.5/32"
    # }
    #
    # TASK [check if a given string is a subnet] ******************************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:15
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.0.0/16"
    # }
    #
    # TASK [Get the number of subnets a given subnet can be split into.] ******************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:20
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "16"
    # }
    #
    # TASK [Get a 1st subnet] *************************************************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:25
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.0.0/20"
    # }
    #
    # TASK [Get a last subnet] ************************************************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:30
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.240.0/20"
    # }
    #
    # TASK [Get biggest subnet that contains that given IP address.] **********************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:35
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.144.0/20"
    # }
    #
    # TASK [Get 1st smaller subnet by specifying 0 as index number] ***********************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:40
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.128.0/18"
    # }
    #
    # TASK [Get last subnet] **************************************************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:45
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "192.168.144.4/31"
    # }
    #
    # TASK [The rank of the IP in the subnet (the IP is the 36870nth /32 of the subnet)] **************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:50
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "36870"
    # }
    #
    # TASK [The rank in the /24 that contain the address] *********************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:55
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "6"
    # }
    #
    # TASK [An IP with the subnet in the first /30 in a /24] ******************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:60
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "1"
    # }
    #
    # TASK [he fifth subnet /30 in a /24] *************************************************************************
    # task path: /Users/amhatre/ansible-collections/playbooks/test_ipsubnet.yaml:65
    # Loading collection ansible.utils from /Users/amhatre/ansible-collections/collections/ansible_collections/ansible/utils
    # ok: [localhost] => {
    #     "msg": "5"
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
