# Northbridge change request NB 206

## Exhibit A · A vendor proposes a rollback

**Fictional ticket, 16 November 2026.** A support engineer reports that their old demo uses PyJWT 2.13.0 and proposes replacing the value in Friday’s dependency file. Their comment reads “It is pinned and the login demo passed on my laptop.” The change has not been merged. The proposed value is stored as plain text in `exercises/day06-proposal.case` for the offline checker. Never install that exhibit.

**Offline advisory record, prepared 16 November 2026.** The following is a trainer-curated extract of facts from the PyJWT maintainer. It is a single finding. No scanner output has been invented.

| Field | Offline evidence |
| --- | --- |
| Project and alias | PyJWT • GHSA-9v7f-9g4p-ffgj • CVE-2026-102267 |
| Affected and patched | The maintainer lists versions up to and including 2.13.0 as affected. The first patched release for this advisory is 2.14.0. |
| Affected code | The public key client, `PyJWKClient`, followed redirects while retrieving signing keys. An attacker would need to influence the trusted endpoint's redirect response. A token key ID by itself is insufficient. |
| Potential effect | A redirect could cause the client to use keys from a different destination. Custom headers supplied to the key endpoint could also be exposed under the affected configuration. |
| Local evidence to inspect | Root `requirements.txt`, `exercises/day05-requirements.txt`, `exercises/day05_identity.py` and `exercises/day05_cognito.py`. Identify the verifier used by each entry point. |
| Scope of the evidence | The snapshot covers this one advisory on the stated date. A live scanner may list other findings. A pinned version, passing API tests and an approved classroom pin each answer a different question. |

A verified Python 3.12 rehearsal had FastAPI 0.162.2 and Starlette 1.10.0 installed. FastAPI declared a dependency on `starlette>=0.46.0`. Pydantic 2.14.3 declared `pydantic-core==2.50.4`. These are fallback inventory observations for machines without network access. Your own installed versions may differ. Find one dependency edge yourself and name the evidence source.

The client asks for a short decision at `docs/day06-decision.md`. Use your actual install result and compare it with Friday’s declared pin. If the class pin already matches a reviewed version, record what the proposed change would undo. [Maintainer advisory](https://github.com/jpadilla/pyjwt/security/advisories/GHSA-9v7f-9g4p-ffgj) · [PyJWT release notes](https://pyjwt.readthedocs.io/en/stable/changelog.html) · [PyPA repeatable installs](https://pip.pypa.io/en/stable/topics/repeatable-installs/).

## Exhibit B · A diagnostic file vanished

**Fictional incident.** A developer says a diagnostic credential appeared in a commit and has now been deleted. The only value used in this lab is `TRAINING_ONLY_NOT_A_CREDENTIAL`. It cannot access any system. The incident generator writes this marker in an isolated local Git repository and configures no remote. The unknowns in the scenario include whether a real-world equivalent would have been pushed, used or copied into a log or image.

Run `python exercises/day06_incident.py` and investigate the resulting folder. If Git is blocked, the following offline snapshot is sufficient to analyse the evidence. Label this route as a supplied exhibit.

| Observation | Recorded fact from the generated history |
| --- | --- |
| Earlier commit subject | Add temporary diagnostic settings |
| Added file | `app/dispatch.local.env` |
| Added line | `DISPATCH_DIAGNOSTIC=TRAINING_ONLY_NOT_A_CREDENTIAL` |
| Later commit subject | Remove diagnostic file from current tree |
| At the tip | The path is absent. The earlier revision still contains the fictional line. |

The trainer expects you to test your own ignore rules with the harmless filename. No real credential, browser session, home directory or personal environment file is part of this investigation.

## Exhibit C · An apparently green package job

The proposed automation is an **inert YAML exhibit** at `docs/day06-workflow-review.yml`. In the review scenario a dependency diagnostic reports an unwanted version, yet a package job can be eligible to build. A reviewer also questions the token scope. Compare the exhibit with your actual `.github/workflows/taskflow-ci.yml`, discovered via `git ls-files .github/workflows`. Some Friday branches contain a better starting workflow. Keep their useful behaviour and repair only the actual weaknesses you observe.

Client constraints for the PR job: use a reviewed read-only checkout, no repository or environment secrets, independent evidence for dependency and test outcomes, and a local image build only after both succeed. Verify the publisher and full action commit in its official release. Where an extra job or step is valid, explain its trust boundary. A developer with permission to change a check can also change its policy, so an independent review remains part of this pilot.

**Publisher evidence for offline rooms, checked 16 November 2026.** These resolved release commits identify the actions in the earlier major version used by the class. With internet access, follow the release tag to the commit in the publisher-owned repository and compare all 40 characters. In an offline room, label the digest as a supplied observation. They are reference data for your edit.

| Action | Publisher release | Reviewed full commit |
| --- | --- | --- |
| actions/checkout | v6.0.2 | `de0fac2e4500dabe0009e67214ff5f5447ce83dd` |
| actions/setup-python | v6.1.0 | `83679a892e2d95755f2dac6acb0bfd1e9ac5d548` |

[Checkout release](https://github.com/actions/checkout/releases/tag/v6.0.2) · [Setup Python release](https://github.com/actions/setup-python/releases/tag/v6.1.0).

The lab provides a dated, one-package offline policy. An optional live audit is a separate form of evidence. [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) · [Workflow semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) · [PyPA pip-audit](https://github.com/pypa/pip-audit).
