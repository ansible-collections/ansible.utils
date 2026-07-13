# Molecule integration (post-migrate)

Integration tests live under `extensions/molecule/<scenario>/`:

- `molecule.yml` — scenario config (localhost/local by default; adjust platforms as needed)
- `converge.yml` — `include_role` of local `content/`
- `content/` — former `tests/integration/targets/<scenario>/` role tree
- `config.yml` — shared defaults (`prerun: false`; ADE/tox owns collection install)

## Run locally

```bash
ade install . -e   # stage git changes first if files were moved
molecule test --all --workers 4
# or via tox matrix cell:
tox --ansible -e integration-py3.12-2.19
```

## Remaining follow-ups

1. Fix scenarios that fail on current ansible-core (e.g. `utils_get_path` filter/argspec issues).
2. Drop this file once the migrate is committed and team docs point at Molecule.
3. Longer term: remove the interim tox `legacy_tox_ini` Molecule override when tox-ansible runs Molecule natively; restore shared content-actions integration workflow if it learns pyproject.toml.

Agent assist: `.agents/skills/molecule-migrate-finalize/SKILL.md`
