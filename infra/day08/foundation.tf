locals {
  name            = "taskflow-${var.team}"
  create_role     = var.enable_host && var.existing_instance_profile == null
  management_port = 0 # Workshop 1: set the outbound transport port needed by SSM.
}

data "aws_subnet" "assigned" {
  id = var.subnet_id
}

data "aws_ami" "approved" {
  count  = var.enable_host ? 1 : 0
  owners = ["amazon"]

  filter {
    name   = "image-id"
    values = [coalesce(var.ami_id, "ami-00000000000000000")]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
  lifecycle {
    precondition {
      condition     = var.ami_id != null
      error_message = "Pin the trainer's regional Amazon Linux 2023 standard image ID before planning a host."
    }
  }
}

resource "aws_security_group" "pilot" {
  name_prefix = "${local.name}-"
  description = "TaskFlow training host; managed access through outbound SSM only"
  vpc_id      = data.aws_subnet.assigned.vpc_id

  tags = {
    Name         = "${local.name}-host"
    ReleaseStage = "foundation" # Workshop 2: replace this literal with your input.
  }
}

# New VPC security groups have their default outbound rule removed by this provider.
# This standalone rule is the only intended outbound rule; there are no inbound rules.
resource "aws_vpc_security_group_egress_rule" "management" {
  security_group_id = aws_security_group.pilot.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = local.management_port
  to_port           = local.management_port
  description       = "TLS to public AWS service endpoints"

  lifecycle {
    precondition {
      condition     = local.management_port == 443
      error_message = "Review the transport used by the SSM agent. Choose its single TLS egress port before applying."
    }
  }
}

resource "aws_instance" "pilot" {
  count                       = var.enable_host ? 1 : 0
  ami                         = data.aws_ami.approved[0].id
  instance_type               = "t3.micro"
  subnet_id                   = data.aws_subnet.assigned.id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.pilot.id]
  iam_instance_profile        = local.create_role ? aws_iam_instance_profile.pilot[0].name : var.existing_instance_profile

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  credit_specification {
    cpu_credits = "standard"
  }
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    encrypted             = true
    delete_on_termination = true
    tags = {
      Name   = "${local.name}-root"
      Team   = var.team
      Owner  = var.team
      RetireOn = var.retire_on
      Project  = "TaskFlow"
    }
  }
  tags = { Name = local.name }

  depends_on = [aws_vpc_security_group_egress_rule.management, aws_iam_role_policy.agent]
}

resource "aws_ebs_volume" "bookings" {
  count             = var.enable_host ? 1 : 0
  availability_zone = data.aws_subnet.assigned.availability_zone
  type              = "gp3"
  size              = 4
  encrypted         = true
  tags              = { Name = "${local.name}-bookings" }
}

resource "aws_volume_attachment" "bookings" {
  count       = var.enable_host ? 1 : 0
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.bookings[0].id
  instance_id = aws_instance.pilot[0].id
}
