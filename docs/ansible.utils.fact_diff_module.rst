.. _ansible.utils.fact_diff_module:


***********************
ansible.utils.fact_diff
***********************

**Find the difference between currently set facts**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Compare two facts or variables and get a diff




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
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
                        <div>The second fact to be used in the comparison</div>
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
                        <div>The first fact to be used in the comparison</div>
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
                        <div>The diff plugin to use, in collection format</div>
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
                        <div>Parameters passed to the diff plugin</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Skip lines matching these regular expressions</div>
                        <div>Matches will be removed prior to the diff</div>
                        <div>If the provided <em>before</em> and <em>after</em> are a string, they will be split</div>
                        <div>Each entry in each list will be cast to a string for the comparison</div>
                </td>
            </tr>


    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)
