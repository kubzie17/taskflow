# Cost desk | Northbridge architecture panel

US East (N. Virginia), us-east-1. USD public list reference checked 16 November 2026. Model month = 730 hours. Before tax and credits. Your sandbox uses the owner's approved Region. Re-price if the design Region changes.

| Item | Unit | USD per unit | Source |
|---|---|---:|---|
| EC2 Linux t3.micro | instance-hour | 0.0104 | [EC2](https://aws.amazon.com/ec2/instance-types/t3/) |
| EBS gp3 baseline | GB-month | 0.08 | [EBS](https://aws.amazon.com/ebs/pricing/) |
| EBS standard snapshot | incremental GB-month | 0.05 | [EBS](https://aws.amazon.com/ebs/pricing/) |
| Public IPv4 in use | address-hour | 0.005 | [IPv4](https://aws.amazon.com/vpc/pricing/) |
| Fargate Linux/x86 vCPU | vCPU-hour | 0.0404784 | [Fargate](https://aws.amazon.com/fargate/pricing/) |
| Fargate Linux/x86 memory | GB-hour | 0.004446 | [Fargate](https://aws.amazon.com/fargate/pricing/) |
| Application Load Balancer | LB-hour | 0.0225 | [ELB](https://aws.amazon.com/elasticloadbalancing/pricing/) |
| ALB capacity assumption | LCU-hour | 0.008 | [ELB](https://aws.amazon.com/elasticloadbalancing/pricing/) |
| Aurora Serverless v2 Standard | ACU-hour | 0.12 | [Aurora](https://aws.amazon.com/rds/aurora/pricing/) |
| Aurora Standard storage | GB-month | 0.1 | [Aurora](https://aws.amazon.com/rds/aurora/pricing/) |
| Aurora Standard I/O | million operations | 0.2 | [Aurora](https://aws.amazon.com/rds/aurora/pricing/) |
| Interface endpoints | endpoint-AZ-hour | 0.01 | [PrivateLink](https://aws.amazon.com/privatelink/pricing/) |
| Interface endpoint data | GB processed | 0.01 | [PrivateLink](https://aws.amazon.com/privatelink/pricing/) |
| ECR private image storage | GB-month | 0.1 | [ECR](https://aws.amazon.com/ecr/pricing/) |
| Secrets Manager secret | secret-month | 0.4 | [Secrets](https://aws.amazon.com/secrets-manager/pricing/) |
| Secrets Manager requests | 10,000 calls | 0.05 | [Secrets](https://aws.amazon.com/secrets-manager/pricing/) |
| CloudWatch Logs ingestion | GB ingested | 0.5 | [Logs](https://aws.amazon.com/cloudwatch/pricing/) |
| S3 gateway endpoint | endpoint-hour | 0 | [Gateway](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html) |

## Build your estimate
Enter monthly quantities in the workbook. For hourly items multiply count × hours × capacity per unit. Enter 0 when unused. State exclusions and explain your assumptions. Fargate hourly equivalents use Linux/x86 per-second rates. Two continuously allocated IPv4 addresses use 1,460 address-hours. Aurora charges for capacity on each active writer/reader. ALB hours and capacity are separate. Each interface endpoint is billed in each enabled AZ. An S3 gateway endpoint carries no additional endpoint fee; storage, requests and traffic can still be charged.

Examples of exclusions to examine: cross-AZ/internet traffic, log retention, surplus T3 CPU credits, extra gp3 performance, backups beyond allowances, additional services and tax. Separately price additions before including them in a recommendation.

## Hands-on AWS activity
The only cloud creation candidate is a fictional object in an approved existing unversioned private S3 Standard bucket. Illustrative US East S3 Standard rates: first tier $0.023/GB-month, PUT/LIST $0.005/1,000, GET $0.0004/1,000. Console navigation may make additional requests and transfer may apply. Delete the exact key and verify. Account credits and allowances are individual. No account purchase is required.
[S3 pricing](https://aws.amazon.com/s3/pricing/) · [Free Tier and plans](https://aws.amazon.com/free/free-tier-faqs/) · [Pricing Calculator](https://calculator.aws/)
