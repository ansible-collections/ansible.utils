.. _ansible.utils.fact_diff_filter:


***********************
ansible.utils.fact_diff
***********************

**Find the difference between currently set facts**


Version added: 2.12.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Compare two facts or variables and get a diff.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>after</b>
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
                        <div>The second fact to be used in the comparison.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>before</b>
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
                        <div>The first fact to be used in the comparison.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>common</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Show all common lines.</div>
                </td>
            </tr>
            <tr>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Configure and specify the diff plugin to use</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"ansible.utils.native"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The diff plugin to use, in fully qualified collection name format.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vars</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Parameters passed to the diff plugin.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>skip_lines</b>
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
                        <div>Skip lines matching these regular expressions.</div>
                        <div>Matches will be removed prior to the diff.</div>
                        <div>If the provided <em>before</em> and <em>after</em> are a string, they will be split.</div>
                        <div>Each entry in each list will be cast to a string for the comparison</div>
                </td>
            </tr>


    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Set fact
      ansible.builtin.set_fact:
        before:
          a:
            b:
              c:
                d:
                  - 0
                  - 1
        after:
          a:
            b:
              c:
                d:
                  - 2
                  - 3

    - name: Show the difference in json format
      ansible.builtin.set_fact:
        result: "{{before | ansible.utils.fact_diff(after)}}"

    # TASK [Show the difference in json format] **********************************************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "result": [
    #             "--- before",
    #             "+++ after",
    #             "@@ -3,8 +3,8 @@",
    #             "         "b": {",
    #             "             "c": {",
    #             "                 "d": [",
    #             "-                    0,",
    #             "-                    1",
    #             "+                    2,",
    #             "+                    3",
    #             "                 ]",
    #             "             }",
    #             "         }",
    #             ""
    #         ]
    #     },
    #     "changed": false
    # }

    - name: Set fact
      ansible.builtin.set_fact:
        before: "{{ before|ansible.utils.to_paths }}"
        after: "{{ after|ansible.utils.to_paths }}"

    - name: Show the difference in path format
      ansible.builtin.set_fact:
        result: "{{before | ansible.utils.fact_diff(after)}}"

    # TASK [Show the difference in path format] **********************************************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "result": [
    #             "--- before",
    #             "+++ after",
    #             "@@ -1,4 +1,4 @@",
    #             " {",
    #             "-    "a.b.c.d[0]": 0,",
    #             "-    "a.b.c.d[1]": 1",
    #             "+    "a.b.c.d[0]": 2,",
    #             "+    "a.b.c.d[1]": 3",
    #             " }",
    #             ""
    #         ]
    #     },
    #     "changed": false
    # }

    - name: Set fact
      ansible.builtin.set_fact:
        before: "{{ before|to_nice_yaml }}"
        after: "{{ after|to_nice_yaml }}"

    - name: Show the difference in yaml format
      ansible.builtin.set_fact:
        result: "{{before | ansible.utils.fact_diff(after)}}"

    # TASK [Show the difference in yaml format] **********************************************************************************************
    # ok: [localhost] => {
    #     "ansible_facts": {
    #         "result": [
    #             "--- before",
    #             "+++ after",
    #             "@@ -1,2 +1,2 @@",
    #             "-a.b.c.d[0]: 0",
    #             "-a.b.c.d[1]: 1",
    #             "+a.b.c.d[0]: 2",
    #             "+a.b.c.d[1]: 3",
    #             ""
    #         ]
    #     },
    #     "changed": false
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
                    <b>result</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>Returns diff between before and after facts.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ashwini Mhatre ((@amhatre))


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
