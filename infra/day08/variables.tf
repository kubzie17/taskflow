variable "aws_region" {
  description = "Training Region named by the account owner."
  type        = string
  default     = "eu-west-1"
}

variable "approved_account_id" {
  description = "Account ID supplied privately by the owner. Scoped provider guard."
  type        = string
  validation {
    condition     = can(regex("^[0-9]{12}$", var.approved_account_id))
    error_message = "Supply the approved 12-digit training account ID in your private tfvars."
  }
}

variable "team" {
  description = "Trainer-assigned unique, account-wide group alias; use the same alias on Days 8–10."
  type        = string
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,18}[a-z0-9]$", var.team))
    error_message = "Use an assigned 4–20 character lowercase alias starting with a letter and ending with a letter or digit."
  }
}

variable "subnet_id" {
  description = "Existing approved subnet with a route to an internet gateway."
  type        = string
  validation {
    condition     = can(regex("^subnet-([0-9a-f]{8}|[0-9a-f]{17})$", var.subnet_id))
    error_message = "Use the real assigned subnet ID from the approved Region."
  }
}

variable "ami_id" {
  description = "Pinned Amazon-owned AL2023 x86_64 standard image ID for this Region."
  type        = string
  default     = null
  validation {
    condition     = var.ami_id == null ? true : can(regex("^ami-([0-9a-f]{8}|[0-9a-f]{17})$", var.ami_id))
    error_message = "Use the Region-specific image ID the trainer resolved."
  }
}

variable "enable_host" {
  description = "Default true. False is the initial network-only recovery route for a real compute blocker."
  type        = bool
  default     = true
}

variable "existing_instance_profile" {
  description = "Optional owner-provided EC2 instance profile name. Leave null for the course-managed role."
  type        = string
  default     = null
  validation {
    condition     = var.existing_instance_profile == null ? true : can(regex("^[A-Za-z0-9+=,.@_-]{1,128}$", var.existing_instance_profile))
    error_message = "Enter an approved profile name, not an ARN, or leave null."
  }
}

variable "retire_on" {
  description = "Agreed cleanup date in the course resource ledger."
  type        = string
  default     = "2026-11-27"
  validation {
    condition     = can(formatdate("YYYY-MM-DD", "${var.retire_on}T00:00:00Z"))
    error_message = "Use an ISO calendar date such as 2026-11-27."
  }
}

variable "release_stage" {
  description = "Release stage tag for the security group"
  type        = string
  default     = "foundation"
  validation {
    condition     = var.release_stage == "foundation" || var.release_stage == "deploy-ready"
    error_message = "Release stage must be 'foundation' or 'deploy-ready'."
  }
}

