# About

[collective.mastodon](https://github.com/collective/collective.mastodon) is a package providing a [Plone](https://plone.org) content rules action to post a status using a Mastodon account.

## Code Health
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
