locals {
  registry = "${var.approved_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}

# Day 9: the fixed script GitHub may run on the host. Only the digest can vary.
resource "aws_ssm_document" "deploy-cool-squad" {
  name            = "TaskFlow-Day09-${var.team}"
  document_type   = "Command"
  document_format = "YAML"
  content         = <<-DOC
    schemaVersion: "2.2"
    description: Deploy a checked TaskFlow image by digest.
    parameters:
      ImageDigest:
        type: String
        allowedPattern: "^sha256:[a-f0-9]{64}$"
      AppEnvironment:
        type: String
        allowedPattern: "^training$"
      AppPort:
        type: String
        allowedPattern: "^8055$"
    mainSteps:
      - action: aws:runShellScript
        name: deploy
        inputs:
          timeoutSeconds: "600"
          runCommand:
            - |
              set -euo pipefail
              IMAGE=${local.registry}/${var.ecr_repository}@{{ ImageDigest }}
              # Refuse to start unless the data folder is on the bookings volume.
              SERIAL=$(lsblk -dn -o SERIAL "$(findmnt -n -o SOURCE --target /srv/taskflow-data/app)")
              test "$SERIAL" = "${replace(aws_ebs_volume.bookings-cool-squad[0].id, "-", "")}"
              # Secret goes to memory-backed /run, readable only by the container user.
              install -d -m 700 -o 10001 -g 10001 /run/taskflow
              aws ssm get-parameter --region ${var.aws_region} --name /taskflow/${var.team}/runtime-identity --with-decryption --query Parameter.Value --output text > /run/taskflow/identity.json
              chown 10001:10001 /run/taskflow/identity.json
              chmod 400 /run/taskflow/identity.json
              aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${local.registry}
              docker pull "$IMAGE"
              docker rm -f taskflow || true
              docker run -d --name taskflow --read-only --cap-drop ALL --security-opt no-new-privileges --tmpfs /tmp -p 127.0.0.1:{{ AppPort }}:8000 -e APP_ENVIRONMENT={{ AppEnvironment }} -e TASKFLOW_DB=/var/lib/taskflow/taskflow.db -e TASKFLOW_IDENTITY_FILE=/run/secrets/identity.json --mount type=bind,src=/run/taskflow/identity.json,dst=/run/secrets/identity.json,readonly --mount type=bind,src=/srv/taskflow-data/app,dst=/var/lib/taskflow "$IMAGE"
              curl -fsS --retry 15 --retry-delay 2 --retry-all-errors http://127.0.0.1:{{ AppPort }}/health
  DOC
}

output "ssm_document_name" {
  value = aws_ssm_document.deploy-cool-squad.name
}
