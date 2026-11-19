# Day 10 progressive hints

Try a hypothesis, a command and an interpretation before opening the next hint. These prompts are separate from challenge cards.

<details><summary>Monitoring hint 1</summary>
Separate host reachability, container state and protected application behaviour. Which observation is closest to the symptom?
</details>
<details><summary>Monitoring hint 2</summary>
`docker ps` shows running containers. `docker ps -a` also shows stopped ones. Compare the status and timestamp with the request failure.
</details>
<details><summary>Monitoring hint 3</summary>
Inspect the named container's exit state and recent lifecycle logs. If the proposed recovery is a start operation, verify that its identity file and EBS mount still exist before asking the trainer to approve it.
</details>
<details><summary>Recovery hint 1</summary>
Write a timeline with A, checkpoint, B and the incident. Which source did the recovery operation use?
</details>
<details><summary>Recovery hint 2</summary>
Compare actual IDs using `day10_db.py inspect`, then compare the API on the original and isolated recovery ports. A valid backup can still have an unacceptable recovery-point age.
</details>
<details><summary>Recovery hint 3</summary>
A stopped original does not erase its data. The recovered process uses another file. Keep record loss in the restored view separate from records still present in the original.
</details>
<details><summary>Cleanup hint</summary>
An IAM denial is not a missing resource. A stopped instance is not a deleted volume. Check the exact ID, current identity and service-specific response, then record unresolved resources with an owner.
</details>
