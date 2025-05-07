# RHEL Writers Template

## Writing Templates

The data the template has access to has the following schema:

```json
{
    "advisory_name": "2025:XYZ",
    "advisory_ship_date": "2025-01-01",
    "advisory": {
        "spec": {
            "type": "...",
            "issues": [...],
            ...
        }
    }
}
```

So templates should access `advisory.spec` for almost anything:

```yaml
synopsis: |
    {% if advisory.spec.type == "RHSA" %}
        {{ advisory.spec.severity }}: {{ advisory.spec.product_name }} security update
    {% else %}
        {{ advisory.spec.product_name }} bug fix and enhancement update
    {% endif %}
...
```

To see a list of available fields, see the advisories at
[RelEng Advisories Repository](https://gitlab.cee.redhat.com/releng/advisories).


## Manual Testing
To manually test the templates use the script `manual-test.py`. This script uses advisories from
[RelEng Advisories Repository](https://gitlab.cee.redhat.com/releng/advisories)
to replicate the behaviour of Konflux when creating advisories. The script also uses a
template from this repository and combines both to show you the result of the template
given the data on the advisory specified.

Before running the test script create the environment to install its dependencies:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements.txt
```

*Note*: before executing the script you need to `source ven/bin/activate`

These are some usage examples for the testing script:

* Locally:

```bash
$ git clone https://gitlab.cee.redhat.com/releng/advisories.git --depth=1
$ git clone https://github.com/konflux-ci/release-service-utils.git --depth=1
$ python manual-test.py --advisory file://advisories/data/advisories/cluster-observabilit-tenant/2025/1609/advisory.yaml --template file://default/rhea.yaml
synopsis
==================================================
Bug fix and enhancement update
==================================================

description
==================================================
[...omitted content...]
```

* Using HTTP (which reaches for the files over the internet):

```bash
$ git clone https://github.com/konflux-ci/release-service-utils.git --depth=1
$ python manual-test.py \
    --advisory https://gitlab.cee.redhat.com/releng/advisories/-/raw/main/data/advisories/cluster-observabilit-tenant/2025/1609/advisory.yaml \
    --template https://gitlab.cee.redhat.com/hemartin/rhel-writers-templates/-/raw/main/default/rhea.yaml
synopsis
==================================================
Bug fix and enhancement update
==================================================

description
==================================================
[...omitted content...]
```

## Debugging Problems
