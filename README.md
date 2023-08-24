<div align="center"><img alt="logo" src="./docs/_static/images/icon.png" width="70" /></div>

<h1 align="center">collective.mastodon</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/collective.mastodon)](https://pypi.org/project/collective.mastodon/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.mastodon)](https://pypi.org/project/collective.mastodon/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.mastodon)](https://pypi.org/project/collective.mastodon/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.mastodon)](https://pypi.org/project/collective.mastodon/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.mastodon)](https://pypi.org/project/collective.mastodon/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.mastodon)](https://pypi.org/project/collective.mastodon/)

[![Meta](https://github.com/collective/collective.mastodon/actions/workflows/meta.yml/badge.svg)](https://github.com/collective/collective.mastodon/actions/workflows/meta.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.mastodon)](https://github.com/collective/collective.mastodon)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.mastodon?style=social)](https://github.com/collective/collective.mastodon)

</div>

**collective.mastodon** is a package providing a [Plone](https://plone.org/) content rules action to post a status to a Mastodon instance.


# Installation

This package supports Plone sites using Volto and ClassicUI.

For proper Volto support, the requirements are:

* plone.restapi >= 8.34.0
* Volto >= 16.10.0

Add **collective.mastodon** to the Plone installation using `pip`:

```bash
pip install collective.mastodon
```

or add it as a dependency on your package's `setup.py`

```python
    install_requires = [
        "collective.mastodon",
        "Plone",
        "plone.restapi",
        "setuptools",
    ],
```

## Configuration

### Obtaining an Access Token
Before you can use this package, you have to register an application on Mastodon.
To do so, log in to your account, visit `settings/applications/new` and create the application. (Please select `read` and `write` scopes, and keep the default `Redirect URI`).
Go to the newly created application page and copy the value of `Your access token`.

### Configuring Plone

This package is configured via the `MASTODON_APPS` environment variable which should contain a valid JSON array with your Mastodon Application information.

Each application registration requires the following information:

| Key | Description | Example Value |
| -- | -- | -- |
| name | Identifier for the application | localhost-user |
| instance | URL of your instance, without the trailing slash | http://localhost |
| token | Access token of your Mastodon Application | jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M |
| user | User on the Mastodon instance. (Only used to generate a friendly name on Plone) | user |

Using the information above, the environment variable would look like:

```shell
MASTODON_APPS='[{"name": "localhost-user","instance":"http://localhost","token":"jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M","user":"user"}]'
```

### Starting Plone

Now, you can start your local Plone installation with:

```shell
MASTODON_APPS='[{"name": "localhost-user","instance":"http://localhost","token":"jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M","user":"user"}]' make start
```

or, if you are using a `docker compose` configuration, add the new environment variable under the `environment` key:

```yaml
    environment:
      - MASTODON_APPS='[{"name": "localhost-user","instance":"http://localhost","token":"jutbgrhNDS1EvUvpoHD0ox4a7obSCT9_IpliStv799M","user":"user"}]'
```

After start-up visit the `Content Rules` Control Panel, and create a new content rule.

No additional configuration is needed for Volto support.

# Contributing

If you want to help with the development (improvement, update, bug-fixing, ...) of `collective.mastodon` this is a great idea!

- [Issue Tracker](https://github.com/collective/collective.mastodon/issues)
- [Source Code](https://github.com/collective/collective.mastodon/)
- [Documentation](https://collective.github.io/collective.mastodon)

We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.

## Local Development

You need a working `python` environment (system, `virtualenv`, `pyenv`, etc) version 3.8 or superior.

Then install the dependencies and a development instance using:

```bash
make build
```
### Update translations

```bash
make i18n
```

### Format codebase

```bash
make format
```

### Run tests

Testing of this package is done with [`pytest`](https://docs.pytest.org/) and [`tox`](https://tox.wiki/).

Run all tests with:

```bash
make test
```

Run all tests but stop on the first error and open a `pdb` session:

```bash
./bin/tox -e test -- -x --pdb
```

Run only tests that match `TestAppDiscovery`:

```bash
./bin/tox -e test -- -k TestAppDiscovery
```

Run only tests that match `TestAppDiscovery`, but stop on the first error and open a `pdb` session:

```bash
./bin/tox -e test -- -k TestAppDiscovery -x --pdb
```

## Translations

This product has been translated into:

- English (Érico Andrei)
- Português do Brasil (Érico Andrei)

# License

The project is licensed under GPLv2.

# One Last Thing

Originally Made in São Paulo, Brazil, with love, by your friends @ Simples Consultoria.

Now maintained by the [Plone Collective](https://github.com/collective)
