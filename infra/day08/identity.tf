resource "aws_iam_role" "pilot-cool-squad" {
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
resource "aws_iam_role_policy" "agent-cool-squad" {
  count = local.create_role ? 1 : 0
  name  = "taskflow-agent"
  role  = aws_iam_role.pilot-cool-squad[0].id
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

# Day 9: read this team's runtime identity and pull this team's image from ECR.
resource "aws_iam_role_policy" "runtime-cool-squad" {
  count = local.create_role ? 1 : 0
  name  = "taskflow-runtime"
  role  = aws_iam_role.pilot-cool-squad[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "ssm:GetParameter"
        Resource = "arn:aws:ssm:${var.aws_region}:${var.approved_account_id}:parameter/taskflow/${var.team}/runtime-identity"
      },
      {
        # Login to ECR cannot be scoped to one repository.
        Effect   = "Allow"
        Action   = "ecr:GetAuthorizationToken"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"]
        Resource = "arn:aws:ecr:${var.aws_region}:${var.approved_account_id}:repository/${var.ecr_repository}"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "pilot-cool-squad" {
  count = local.create_role ? 1 : 0
  name  = "${local.name}-profile"
  role  = aws_iam_role.pilot-cool-squad[0].name
}
