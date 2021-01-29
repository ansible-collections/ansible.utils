======================================
Ansible Utils Collection Release Notes
======================================

.. contents:: Topics


v2.0.0
======

Breaking Changes / Porting Guide
--------------------------------

- If added custom sub plugins in your collection move from old location `plugins/<sub-plugin-name>` to the new location `plugins/sub_plugins/<sub-plugin-name>` and update the imports as required
- Move sub plugins cli_parsers, fact_diff and validate to `plugins/sub_plugins` folder
- The `cli_parsers` sub plugins folder name is changed to `cli_parse` to have consistent naming convention, that is all the cli_parse subplugins will now be in `plugins/sub_plugins/cli_parse` folder

v1.0.1
======

Minor Changes
-------------

- Move CHANGELOG.rst file under changelogs folder as required

v1.0.0
======

Minor Changes
-------------

- Add cli_parse module and plugins (https://github.com/ansible-collections/ansible.utils/pull/28)
- Added fact_diff plugin and sub plugin
- Added validate module/lookup/filter/test plugin to validate data based on given criteria

Bugfixes
--------

- linting and formatting for CI

New Plugins
-----------

Lookup
~~~~~~

- get_path - Retrieve the value in a variable using a path
- index_of - Find the indices of items in a list matching some criteria
- to_paths - Flatten a complex object into a dictionary of paths and values
- validate - Validate data with provided criteria

New Modules
-----------

- cli_parse - Parse cli output or text using a variety of parsers
- fact_diff - Find the difference between currently set facts
- update_fact - Update currently set facts
- validate - Validate data with provided criteria
