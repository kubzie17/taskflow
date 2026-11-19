terraform {
  required_version = ">= 1.9.0, < 2.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 6.73.0"
    }
  }
}

provider "aws" {
  region              = var.aws_region
  allowed_account_ids = [var.approved_account_id]

  default_tags {
    tags = {
      Project     = "TaskFlow"
      Environment = "training"
      ManagedBy   = "Terraform"
      Team        = var.team
      Owner       = var.team
      RetireOn    = var.retire_on
    }
  }
}
