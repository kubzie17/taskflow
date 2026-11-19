# Day 9 configuration worksheet

Complete the two blank columns in a private copy. For sensitive values, record the name and purpose only.

| Value | Used by | Where should it be configured and why | What happens if it is missing |
|---|---|---|---|
| PYTHON_VERSION | Python setup during CI | | |
| AWS_REGION | AWS CLI and credential action | | |
| AWS_ROLE_ARN | GitHub's OIDC exchange | | |
| ECR_REPOSITORY | Publishing and host image pull | | |
| IMAGE_TAG | One pipeline run | | |
| IMAGE_DIGEST | The release operation | | |
| INSTANCE_ID | SSM deployment target | | |
| APP_PORT | Host loopback and tunnel | | |
| APP_ENVIRONMENT | Application startup | | |
| TASKFLOW_DB | SQLite file path inside Docker | | |
| TASKFLOW_IDENTITY_FILE | Identity file path inside Docker | | |
| DEMO_RELEASE_NOTE | Optional GitHub secret demonstration | | |
| Runtime signing key and password records | Protected application | | |

Compare workflow-level `env`, the test job's `env`, and the publish step's mapping from `vars`. Which values are decided when the image is built, when a release is selected, and when the application starts? Which value can change while the image digest stays the same?

GitHub configuration variables are readable configuration. Secrets are encrypted at rest and have controls on availability, but a workflow that receives a secret can misuse it. Masking reduces accidental log exposure and does not cover every transformed value. The demonstration checks presence without printing the phrase. The app's identity bundle is retrieved separately by the host role.

Required AWS configuration fails early with a named error. `PYTHON_VERSION` has a documented `3.12` default and `DEMO_RELEASE_NOTE` is an optional teaching value. Discuss why a silent default for the account or instance would be a poor deployment choice.
