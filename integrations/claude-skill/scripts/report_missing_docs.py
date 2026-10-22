#!/usr/bin/env python3
"""Best-effort public documentation hint; detaches and never retries or prints."""

import argparse
import ipaddress
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

REPORT_URL = "https://api.llmref.org/v1/documentation-reports"


def clean_payload(value):
    payload = {k: v for k, v in value.items() if v is not None}
    if set(payload) - {"project", "version", "docs_url", "llms_txt_url"}:
        return None
    project = payload.get("project", "")
    if not isinstance(project, str) or not re.fullmatch(
        r"[A-Za-z0-9@/._+ -]{1,120}", project
    ):
        return None
    if "version" in payload and (
        not isinstance(payload["version"], str) or len(payload["version"]) > 80
    ):
        return None
    for key in ("docs_url", "llms_txt_url"):
        if key not in payload:
            continue
        value = payload[key]
        if not isinstance(value, str) or len(value) > 2048:
            return None
        try:
            url = urllib.parse.urlsplit(value)
            host = (url.hostname or "").lower().rstrip(".")
            if (
                url.scheme != "https"
                or url.username
                or url.password
                or url.query
                or url.port not in (None, 443)
                or "." not in host
            ):
                return None
            if re.fullmatch(
                r"(?:0[xX][0-9A-Fa-f]+|[0-9]+)(?:\.(?:0[xX][0-9A-Fa-f]+|[0-9]+))*", host
            ):
                return None
            if any(
                host == s or host.endswith("." + s)
                for s in ("localhost", "local", "internal", "test", "invalid", "onion")
            ):
                return None
            try:
                ipaddress.ip_address(host)
            except ValueError:
                pass
            else:
                return None
            if key == "llms_txt_url" and not url.path.endswith("/llms.txt"):
                return None
            payload[key] = urllib.parse.urlunsplit(url._replace(fragment=""))
        except ValueError:
            return None
    return payload


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def deliver(payload):
    payload = clean_payload(payload)
    if payload is None:
        return
    request = urllib.request.Request(
        REPORT_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "llmref-skill/0.1 (+https://llmref.org)",
        },
        method="POST",
    )
    try:
        with urllib.request.build_opener(NoRedirect()).open(
            request, timeout=1
        ) as response:
            response.read(1024)
    except Exception:
        pass


def main():
    if os.getenv("LLMREF_DISABLE_REPORTING", "").lower() in {"1", "true", "yes"}:
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project")
    parser.add_argument("--version")
    parser.add_argument("--docs-url")
    parser.add_argument("--llms-txt-url")
    parser.add_argument("--deliver", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.deliver:
        try:
            deliver(json.loads(args.deliver))
        except Exception:
            pass
        return
    payload = clean_payload(
        {
            "project": args.project,
            "version": args.version,
            "docs_url": args.docs_url,
            "llms_txt_url": args.llms_txt_url,
        }
    )
    if payload is None:
        return
    try:
        subprocess.Popen(
            [sys.executable, __file__, "--deliver", json.dumps(payload)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True,
        )
    except Exception:
        pass


if __name__ == "__main__":
    main()
