resource "aws_iam_role" "pilot" {
  count = local.create_role ? 1 : 0
  name  = "${local.name}-node"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# Core agent operations. Parameter-value retrieval is granted separately for one team key on Day 9.
resource "aws_iam_role_policy" "agent" {
  count = local.create_role ? 1 : 0
  name  = "taskflow-agent"
  role  = aws_iam_role.pilot[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ssm:DescribeAssociation", "ssm:DescribeDocument", "ssm:GetDocument",
        "ssm:GetDeployablePatchSnapshotForInstance", "ssm:GetManifest",
        "ssm:ListAssociations", "ssm:ListInstanceAssociations",
        "ssm:PutComplianceItems", "ssm:PutConfigurePackageResult", "ssm:PutInventory",
        "ssm:UpdateAssociationStatus", "ssm:UpdateInstanceAssociationStatus",
        "ssm:UpdateInstanceInformation",
        "ssmmessages:CreateControlChannel", "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel", "ssmmessages:OpenDataChannel",
        "ec2messages:AcknowledgeMessage", "ec2messages:DeleteMessage",
        "ec2messages:FailMessage", "ec2messages:GetEndpoint",
        "ec2messages:GetMessages", "ec2messages:SendReply"
      ]
      Resource = "*"
    }]
  })
}

resource "aws_iam_instance_profile" "pilot" {
  count = local.create_role ? 1 : 0
  name  = "${local.name}-profile"
  role  = aws_iam_role.pilot[0].name
}
