# Day 3 evidence | Will the booking survive?

Challenge: configure TaskFlow and its SQLite storage so that booking records
survive the removal and replacement of the running container.

## Result

PASS. The original booking was retrieved from a new container after the
original container was removed, because the SQLite database lives on a named
Docker volume rather than inside the container's writable layer.

## Storage configuration

| Item | Value |
| --- | --- |
| Database path inside container | `/var/lib/taskflow/taskflow.db` (env `TASKFLOW_DB`) |
| Named volume | `taskflow-data` |
| Mount | `taskflow-data` -> `/var/lib/taskflow` (volume, read-write) |
| Published port | `8083` -> `8000` (loopback) |

Because the volume is mounted at `/var/lib/taskflow` and `TASKFLOW_DB` points
inside that directory, every write goes to the volume. Removing a container
does not remove the volume, so the data outlives the container.

## Container and image evidence

| Evidence required | Value |
| --- | --- |
| Container A ID | `<record from your `docker run` of taskflow-a — removed before capture>` |
| Container B ID | `a151cb8973e9` (name `taskflow-b`) |
| Container A != Container B | Yes — different containers |
| Image ID (both containers) | `sha256:2dceb9af2487137ed90f3e63217f5a17cbb44cbbf2ce6a4a29af411521228f50` (tag `taskflow:day3`) |
| Image match | Yes — Container B's image SHA equals the `taskflow:day3` image SHA |

Note: Container A was stopped and removed before this evidence was captured, so
its container ID could not be read back from the live Docker state. Fill in the
ID you recorded when you started Container A.

## Original booking

| Field | Value |
| --- | --- |
| Booking ID | `1` |
| Exact title | `Replace brake pads on van VX12` |

A second booking (`id 2`, `Replace brake pads on van VX58 LMO`) is also present
on the volume; the acceptance criteria track booking `1` as the original.

## Retrieval after replacement

`GET /health` on Container B:

```text
HTTP 200
{"status":"ok","service":"taskflow"}
```

`GET /tasks` on Container B:

```text
[{"title":"Replace brake pads on van VX12","id":1},
 {"title":"Replace brake pads on van VX58 LMO","id":2}]
```

Verification helper (`exercises/check_booking.py`):

```text
py -3.12 exercises/check_booking.py 1 "Replace brake pads on van VX12" --port 8083

GET /health: HTTP 200, status ok
PASS: booking 1 matches 'Replace brake pads on van VX12'
```

## Commands used to capture this evidence

```powershell
docker ps -a --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'
docker images taskflow
docker volume ls
docker inspect taskflow-b --format '{{range .Mounts}}{{.Type}} | {{.Name}} | {{.Source}} -> {{.Destination}}{{end}}'
docker inspect taskflow-b --format '{{.Image}}'
docker images --no-trunc --format '{{.ID}}' taskflow:day3
py -3.12 exercises/check_booking.py 1 "Replace brake pads on van VX12" --port 8083
```

## Stretch: /health 200 but the booking gone

You can make `/health` return 200 while the booking list is empty by starting a
replacement container **without** the `taskflow-data` volume (or with a
different, empty volume) mounted at `/var/lib/taskflow`. The app's lifespan hook
calls `database.initialise`, which runs `CREATE TABLE IF NOT EXISTS`, so a fresh
empty database is created on startup. `/health` is a static route that always
returns `{"status":"ok"}` and never touches storage, so it reports healthy even
though `GET /tasks` is empty. Cause: health checks the process, not the data —
losing the volume binding silently discards the persisted bookings.
