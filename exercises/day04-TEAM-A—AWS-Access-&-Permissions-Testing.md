# TEAM A — AWS Access & Permissions Testing

**Workbook:** Day 7 Workshop Workbook  
**Worksheet:** 1 Access  
**Your rows:** 4–13

You are already logged into AWS. Your task is to discover which AWS services you can access and inspect.

**Important:** Do not create, delete, launch, upload or change any AWS resources. These are inspection-only tests.

### 1. Portal / Identity (Row 4)

**What to do:**
1. Look at the top-right corner of the AWS Console.
2. Click the account/profile menu.
3. Look for your account details, user or role information.
4. Identify your current AWS Region.

**How to verify:**
- Can you successfully access the AWS Console?
- Can you identify your signed-in user or role?
- Can you see the AWS Region?

**Record:** The type of identity you can identify, the Region and whether access works.

### 2. CLI / Caller Identity (Row 5)

**What to do:**
1. Search for `CloudShell` in the AWS search bar.
2. Open CloudShell.
3. Once the terminal opens, type:

`aws sts get-caller-identity`

4. Press Enter.

**How to verify:**
- Successful: You receive a JSON response containing `UserId`, `Account` and `Arn`.
- Denied: You receive an AccessDenied error.
- If CloudShell cannot launch, record that separately.

**Record:** Whether the command succeeded and whether the ARN identifies a user or assumed role. Do not copy full account identifiers into the shared workbook.

### 3. IAM / Assigned Role (Row 6)

**What to do:**
1. Search for `IAM`.
2. Open IAM.
3. Select **Roles** or **Users**, depending on your identity.
4. Try to locate and inspect your assigned role or user.
5. Open the **Permissions** tab if accessible.

**How to verify:**
- Can you view the relevant role or user?
- Can you inspect any permission policies?
- Do you receive AccessDenied?

**Record:** Allowed, Denied or partially accessible. If you cannot identify your assigned role, say so.

### 4. VPC / Subnet / Route (Row 7)

**What to do:**
1. Search for `VPC`.
2. Click **Your VPCs**.
3. Check whether any VPCs are listed.
4. Open **Subnets**.
5. Open **Route tables**.
6. Try to inspect the configuration of an existing resource.

**How to verify:**
- Can you view VPCs?
- Can you inspect subnets and route tables?
- Is anything blocked?

**Record:** Which sections were accessible, denied or empty.

### 5. Security Groups / Inbound Settings (Row 8)

**What to do:**
1. In VPC, select **Security groups**.
2. Select an existing security group.
3. Open its **Inbound rules** tab.
4. Inspect the ports, protocols and permitted sources.

**How to verify:**
- Can you view security groups?
- Can you read inbound rules?
- Can you identify which traffic is permitted?

**Record:** Whether inbound settings can be inspected. Do not edit any rules.

### 6. EC2 / Volume and Host (Row 9)

**What to do:**
1. Search for `EC2`.
2. Open **Instances**.
3. Check whether instances are visible.
4. Select an existing instance, if available, and inspect its Details and Storage tabs.
5. Open **Elastic Block Store → Volumes**.

**How to verify:**
- Can you view the instance list?
- Can you inspect an existing instance?
- Can you see storage volumes?

**Record:** Allowed, Denied or No resources for each relevant section.

### 7. S3 / Bucket Properties (Row 10)

**What to do:**
1. Search for `S3`.
2. Open **General purpose buckets**.
3. Select an existing bucket you are authorised to inspect.
4. Open **Properties**.
5. Open **Permissions**.

**How to verify:**
- Can you see the bucket list?
- Can you inspect bucket properties?
- Can you view bucket permission settings?

**Record:** What was accessible and any permission errors.

### 8. CloudWatch / Log Groups (Row 11)

**What to do:**
1. Search for `CloudWatch`.
2. Open CloudWatch.
3. Go to **Logs → Log groups**.
4. Check whether log groups are visible.
5. Inspect an existing log group if available.

**How to verify:**
- Can you open the Log groups page?
- Can you list or inspect logs?
- Are you denied access?

**Record:** Whether log-group access works.

### 9. ECS / Services (Row 12)

**What to do:**
1. Search for `Elastic Container Service`.
2. Open **Clusters**.
3. Check for existing clusters.
4. Select a cluster if available.
5. Open its **Services** tab.

**How to verify:**
- Can you see the cluster list?
- Can you inspect services?
- Does AWS deny access?

**Record:** Accessible, Denied or No resources.

### 10. S3 / Object Authority (Row 13)

**What to do:**
1. Return to S3.
2. Open an existing authorised bucket.
3. Select the **Objects** tab.
4. Check whether objects are listed.
5. Select an existing object, if permitted, and inspect its metadata.

**How to verify:**
- Can you list objects?
- Can you inspect object details?
- Are either of these operations denied?

**Record:** What is permitted. Viewing objects does not prove permission to upload, download or delete.

### Completing your workbook

For every row, enter:
- **Region:** The Region being tested.
- **Access status:** Allowed, Denied, Partial, No resources or Not tested.
- **Observed evidence:** What happened when you tried.
- **Expiry / reset / cost:** Any known limitations; otherwise write "Unknown — no changes made".
- **Route / next owner:** What needs checking next and by whom.

**When finished:** Be ready to explain which AWS services Team A could inspect, which were blocked and what would be needed to deploy TaskFlow safely.