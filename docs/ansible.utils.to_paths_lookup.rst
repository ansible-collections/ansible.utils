.. _ansible.utils.to_paths_lookup:


**********************
ansible.utils.to_paths
**********************

**Flatten a complex object into a dictionary of paths and values**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Flatten a complex object into a dictionary of paths and values.
- Paths are dot delimited whenever possible.
- Brackets are used for list indices and keys that contain special characters.
- **to_paths** is also available as a filter plugin.
- Using the parameters below- ``lookup('ansible.utils.to_paths', var, prepend, wantlist``)




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
                    <b>prepend</b>
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
                        <div>Prepend each path entry. Useful to add the initial <em>var</em> name.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>var</b>
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
                        <div>The value of <em>var</em> will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>wantlist</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>If set to <em>True</em>, the return value will always be a list.</div>
                        <div>This can also be accomplished using <code>query</code> or <b>q</b> instead of <code>lookup</code>.</div>
                        <div><a href='https://docs.ansible.com/ansible/latest/plugins/lookup.html'>https://docs.ansible.com/ansible/latest/plugins/lookup.html</a></div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    #### Simple examples

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

    - ansible.builtin.set_fact:
        paths: "{{ lookup('ansible.utils.to_paths', a) }}"

    # TASK [ansible.builtin.set_fact] ********************************************
    # ok: [nxos101] => changed=false
    #   ansible_facts:
    #     paths:
    #       b.c.d[0]: 0
    #       b.c.d[1]: 1
    #       b.c.e[0]: True
    #       b.c.e[1]: False

    - name: Use prepend to add the initial variable name
      ansible.builtin.set_fact:
        paths: "{{ lookup('ansible.utils.to_paths', a, prepend='a') }}"

    # TASK [Use prepend to add the initial variable name] **************************
    # ok: [nxos101] => changed=false
    #   ansible_facts:
    #     paths:
    #       a.b.c.d[0]: 0
    #       a.b.c.d[1]: 1
    #       a.b.c.e[0]: True
    #       a.b.c.e[1]: False


    #### Using a complex object

    - name: Make an API call
      ansible.builtin.uri:
        url: "https://nxos101/restconf/data/openconfig-interfaces:interfaces"
        headers:
          accept: "application/yang.data+json"
        url_password: password
        url_username: admin
        validate_certs: False
      register: result
      delegate_to: localhost

    - name: Flatten the complex object
      ansible.builtin.set_fact:
        paths: "{{ lookup('ansible.utils.to_paths', result.json) }}"

    # TASK [Flatten the complex object] ******************************************
    # ok: [nxos101] => changed=false
    #   ansible_facts:
    #     paths:
    #       interfaces.interface[0].config.enabled: 'true'
    #       interfaces.interface[0].config.mtu: '1500'
    #       interfaces.interface[0].config.name: eth1/71
    #       interfaces.interface[0].config.type: ethernetCsmacd
    #       interfaces.interface[0].ethernet.config['auto-negotiate']: 'true'
    #       interfaces.interface[0].ethernet.state.counters['in-crc-errors']: '0'
    #       interfaces.interface[0].ethernet.state.counters['in-fragment-frames']: '0'
    #       interfaces.interface[0].ethernet.state.counters['in-jabber-frames']: '0'
    #       interfaces.interface[0].ethernet.state.counters['in-mac-control-frames']: '0'
    #       <...>



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this lookup:

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
                    <b>_raw</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">-</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>A dictionary of key value pairs.</div>
                            <div>The key is the path.</div>
                            <div>The value is the value.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
