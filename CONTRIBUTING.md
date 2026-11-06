# Contributing to envguard

Thanks for helping build envguard. **This repository is a work in progress**: only the initial package skeleton, dotenv parser, and schema loader are currently implemented. Commands and integrations listed in the project plan are not complete yet—please check the open issues and coordinate before starting substantial work.

## Get started

```bash
git clone https://github.com/Atharva-devsec/envguard.git
cd envguard
python -m pip install -e ".[dev]"
pytest
```

## Contribution areas

The planned work is split into small, reviewable contributions:

- Scan supported source files for environment-variable usage, including dynamic-access warnings.
- Implement `envguard init` and safe schema generation.
- Implement `envguard check`, JSON output, and `.envguardignore` support.
- Implement `generate`, `sync`, and real-environment `validate` commands.
- Add startup validation examples, Git hooks, pre-commit metadata, and a reusable GitHub Action.
- Improve packaging, documentation, and release automation.

Before working on an item, open or find a GitHub issue describing it and comment that you are taking it on. Keep pull requests focused and avoid duplicating work.

## Project rules

- Never print or store secret values. Diagnostics should include variable names and locations only.
- Return exit code 1 when errors are found; warnings alone should not fail checks.
- Keep runtime dependencies minimal and code typed, readable, and tested with pytest.
- Add tests for behavior changes. Do not use real credentials in fixtures, examples, or logs.
- Update documentation when changing user-facing behavior.

## Pull requests

Include a concise description, tests, and any relevant limitations. Run `pytest` before submitting. If a change affects security or secret handling, include tests proving that values are not leaked.

## License

By contributing, you agree that your contributions will be licensed under the repository's MIT License.
