import argparse
import subprocess
import json
import urllib3
import tempfile

import requests
from yaml import safe_load

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--advisory", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.advisory.startswith("file://"):
        path = args.advisory.replace("file://", "")
        with open(path) as fd:
            advisory_res = fd.read()
        advisory = safe_load(advisory_res)
    else:
        advisory_res = requests.get(args.advisory, verify=False)
        advisory = safe_load(advisory_res.content)

    if args.template.startswith("file://"):
        path = args.template.replace("file://", "")
        with open(path) as fd:
            template_res = fd.read()
        template = safe_load(template_res)
    else:
        template_res = requests.get(args.template, verify=False)
        template = safe_load(template_res.content)

    data = {
        "advisory_name": advisory["metadata"]["name"],
        "advisory_ship_date": advisory["metadata"]["ship_date"],
        "advisory": {
            "spec":  advisory["spec"] | template,
        },
    }

    tmpfile = tempfile.mktemp()
    process = subprocess.run(
        ["python", "release-service-utils/utils/apply_template.py",
            # "--verbose",
            "--data", json.dumps(data),
            "--template", "release-service-utils/templates/advisory.yaml.jinja",
            "--output", tmpfile],
        capture_output=True,
    )

    if args.verbose:
        print(f"DEBUG: raw output from process at file://{tmpfile}")

    if process.returncode != 0:
        print(process.stdout.decode("utf-8"))
        print(process.stderr.decode("utf-8"))
        exit(process.returncode)

    with open(tmpfile) as fd:
        rendered = safe_load(fd.read())

    for key, value in template.items():
        print(key)
        print("=" * 50)
        print(rendered["spec"][key])
        print("=" * 50)
        print()


if __name__ == "__main__":
    main()
