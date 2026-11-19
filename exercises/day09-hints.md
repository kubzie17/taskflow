# Day 9 staged hints

Open the requested section after an initial attempt. Show the trainer your prediction, command and first diagnostic. Pause between hint levels.

## Challenge 1

<details><summary>Hint 1 — Locate the source of each value</summary>

Follow the adapter's existing database-path expression. Use the same environment-reading pattern for the identity file. Check the name of the function defined in the adapter before editing the Docker command.
</details>

<details><summary>Hint 2 — Work out the scopes</summary>

GitHub `vars` makes configured values available to the workflow. An `env` mapping exposes a selected value to the step's process. Compare the provided mappings for the account, repository and port with the empty Region and application-environment fields.
</details>

<details><summary>Hint 3 — Follow the job dependencies</summary>

Read the `needs` keys as prerequisites. A failed dependency check must prevent tests from installing the proposed packages. The package and publish jobs must depend on successful earlier checks. Locate the placeholder test command and choose the full pytest command you used locally.
</details>

## Challenge 2

<details><summary>Hint 1 — Identify the failing layer</summary>

SSM Offline is a host/management problem. An SSM command failure with a reachable session usually has a more specific host, image, secret or mount error. A running container with a failed role probe needs application evidence.
</details>

<details><summary>Hint 2 — Check identity and paths</summary>

Compare the EBS serial with the volume ID, then check the actual filesystem containing the application directory. Compare the exact Parameter Store path and Region with the instance-role policy. Use a query that returns only the parameter version when checking retrieval.
</details>

<details><summary>Hint 3 — Follow the protected process</summary>

Inspect the deployed image reference and its command. Check the mounted identity path and data path without opening the secret file. The host handles AWS retrieval. The container reads the file and uses the protected Day 5 provider. A successful health response alone cannot establish working permissions.
</details>
