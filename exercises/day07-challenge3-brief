# Challenge 3 — Repair the AWS Network Security Rules

**Time: 35 minutes**

## Scenario

Northbridge requires:

- Office users access the edge through HTTPS on TCP 443.
- Only the edge can connect to the application on TCP 8000.
- Only the application can connect to the proposed PostgreSQL database on TCP 5432.
- Unrelated internet callers and workloads must be refused.
- Direct SSH access must not be permitted.

## Step 1 — Copy the starting configuration

```powershell
Copy-Item .\exercises\day07-network.json .\exercises\day07-team-network.json
```

If your team copy already exists, continue working in it.

## Step 2 — Run the checker

```powershell
python -m exercises.day07_network exercises/day07-team-network.json
```

Record which connections fail the specification.

## Step 3 — Open the JSON

Open:

`exercises/day07-team-network.json`

Find:

```json
"inbound_tcp"
```

Review the rules for:

- `sg-edge`
- `sg-app`
- `sg-db`

## Step 4 — Repair the access rules

The fictional office CIDR is:

```text
203.0.113.0/24
```

The rules support a CIDR source or another security group.

For example:

```json
{
  "port": 443,
  "cidr": "203.0.113.0/24"
}
```

Change the necessary rules to match Northbridge's requirements.

Do not change the checker.

## Step 5 — Run the checker again

```powershell
python -m exercises.day07_network exercises/day07-team-network.json
```

Continue until the nine specified flows match the intended access policy.

## Step 6 — Explain your changes

Record:

1. Your original test result.
2. Two incorrect access rules.
3. How you corrected them.
4. Your final test result.
5. One thing the checker does not verify about a real AWS network.

**Success: 9/9 checks matched.**
