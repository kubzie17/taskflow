terraform {
  required_version = ">= 1.9.0, < 2.0.0"
}

variable "team" {
  type    = string
  default = "local-team"
}

# Offline W2: replace the literal stage with a validated release_stage input.
resource "terraform_data" "pilot" {
  input = {
    team        = var.team
    management  = "ssm-outbound-tls"
    release_tag = "foundation"
  }
}

output "observed" {
  value = terraform_data.pilot.output
}
