# Molecule migration next steps

ansible-creator migrated these integration targets into Molecule scenarios:

utils_cli_parse, utils_consolidate, utils_fact_diff, utils_from_xml, utils_get_path, utils_index_of, utils_ipaddr_filter, utils_keep_keys, utils_netaddr_test, utils_param_list_compare, utils_remove_keys, utils_replace_keys, utils_to_paths, utils_to_xml, utils_update_fact, utils_usable_range, utils_validate

Each scenario lives at `extensions/molecule/<target>/` with:

- `molecule.yml` — scenario overrides (shared ansible-native config is `../config.yml`)
- `converge.yml` — `include_role` of playbook-adjacent role `content`
- `roles/content/` — former `tests/integration/targets/<target>/` role tree

Shared across scenarios:

- `extensions/molecule/config.yml` — ansible-native executor + `test_sequence`
- `extensions/molecule/inventory.yml` — localhost with `ansible_connection: local`

## Finalize checklist

1. Confirm shared inventory matches how the old targets ran (localhost vs containers). Override per scenario only when needed.
2. Remove obsolete ansible-test metadata under `roles/content/` (`aliases`, setup-only `meta`) when it no longer applies.
3. Run `molecule test -s <target>` for each migrated scenario (collection root; ADE/venv as usual).
4. Update CI (tox-ansible / GitHub Actions) so migrated targets run via Molecule, not ansible-test integration.
5. Remove empty `tests/integration/targets/` leftovers; decide whether to keep or drop `tests/integration/test_integration.py` / pytest-ansible bridges.
6. Commit the scenario tree and delete any hybrid stubs you no longer need.

Agent assist: open `.agents/skills/molecule-migrate-finalize/SKILL.md` (or ask your coding agent to follow that skill).

# Trigger CI against migrate-integration-to-molecule
