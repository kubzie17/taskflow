Challenge 2 — Will the Booking Survive?
Practical

Scenario

Northbridge Repairs uses TaskFlow to manage customer repair bookings.

A dispatcher creates a booking. Later, the operations team needs to replace the running TaskFlow container during maintenance.

The dispatcher must still be able to retrieve the original booking after the replacement.

Your task

Configure TaskFlow and its SQLite storage so that booking records survive the removal and replacement of the running container.

Acceptance criteria
1. Start TaskFlow in Container A with persistent storage.
2. Create one fictional booking using POST /tasks.
3. Record the booking's original ID and exact title.
4. Stop and remove Container A.
5. Start a new Container B from the same Docker image.
6. Retrieve the original booking using GET /tasks without creating it again.
Evidence required
- Container A's ID.
- Container B's ID — it must be different.
- Image ID used by both containers — it must match.
- Original booking ID and title.
- Evidence of the storage configuration.
- The original booking successfully retrieved after replacement.
Rules: You may create the booking only once. Restarting the same container does not count as replacement. Do not delete any volumes containing data you need to preserve.

Stretch challenge: Can you deliberately reproduce a situation where /health returns HTTP 200 but the original booking has disappeared from the list? Explain what caused it.Challenge 2 — Will the Booking Survive?
Practical

Scenario

Northbridge Repairs uses TaskFlow to manage customer repair bookings.

A dispatcher creates a booking. Later, the operations team needs to replace the running TaskFlow container during maintenance.

The dispatcher must still be able to retrieve the original booking after the replacement.

Your task

Configure TaskFlow and its SQLite storage so that booking records survive the removal and replacement of the running container.

Acceptance criteria
1. Start TaskFlow in Container A with persistent storage.
2. Create one fictional booking using POST /tasks.
3. Record the booking's original ID and exact title.
4. Stop and remove Container A.
5. Start a new Container B from the same Docker image.
6. Retrieve the original booking using GET /tasks without creating it again.
Evidence required
- Container A's ID.
- Container B's ID — it must be different.
- Image ID used by both containers — it must match.
- Original booking ID and title.
- Evidence of the storage configuration.
- The original booking successfully retrieved after replacement.
Rules: You may create the booking only once. Restarting the same container does not count as replacement. Do not delete any volumes containing data you need to preserve.

Stretch challenge: Can you deliberately reproduce a situation where /health returns HTTP 200 but the original booking has disappeared from the list? Explain what caused it.