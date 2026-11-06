# envguard

`envguard` is a minimal Python CLI for validating environment variables from an `env.schema.yaml` file. It is designed to report variable names without exposing values.

## Install for development

```bash
python -m pip install -e ".[dev]"
envguard --version
pytest
```

## Project layout

```text
src/envguard/   Python package
 tests/         pytest tests and fixtures
```

## Schema structure

The schema is a YAML mapping named `variables`. Each variable requires `type`, `required`, `secret`, and `description`; `default` is optional and may be null. Supported types are `string`, `integer`, `number`, and `boolean`. Secret variables cannot define a default.

```yaml
variables:
  API_TOKEN:
    type: string
    required: true
    secret: true
    description: API credential
  DEBUG:
    type: boolean
    required: false
    default: false
    secret: false
    description: Enable debug mode
```

## License

MIT
