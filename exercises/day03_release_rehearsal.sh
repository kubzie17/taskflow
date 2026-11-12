#!/usr/bin/env bash
# Challenge 2: does a booking survive when we replace the running container?
# Run from the project root:  bash exercises/day03_release_rehearsal.sh

# Make a storage area that lives OUTSIDE the container, so data isn't lost when the container goes.
docker volume create tf-sqlite-data

# Start the first instance (A). -d runs it in the background. -p 127.0.0.1:8083:8000 publishes it
# on loopback only (reachable from this machine, not the network). --mount attaches our storage
# volume at /var/lib/taskflow, and -e TASKFLOW_DB tells the app to write its database into that
# mounted folder, so the data lives in the volume rather than inside the container.
docker run -d --name tf-sqlite-data-a -p 127.0.0.1:8083:8000 --mount type=volume,source=tf-sqlite-data,target=/var/lib/taskflow -e TASKFLOW_DB=/var/lib/taskflow/taskflow.db taskflow:4594076

# Give the app a couple of seconds to start up.
sleep 3

# Check the service is alive.
curl -s http://127.0.0.1:8083/health; echo

# Create ONE booking. Note the id it returns (likely 1).
curl -s -X POST http://127.0.0.1:8083/tasks -H 'Content-Type: application/json' -d '{"title":"Inspect bay door Q7"}'; echo

# Confirm the booking is listed on instance A.
curl -s http://127.0.0.1:8083/tasks; echo

# Record instance A's full container id (evidence of the first instance).
docker inspect --format '{{.Id}}' tf-sqlite-data-a

# Record the image id A is running, so we can tie the instance back to the exact image.
docker inspect --format '{{.Image}}' tf-sqlite-data-a

# Show where A's data really lives on the host (evidence that the volume is attached).
docker inspect --format '{{json .Mounts}}' tf-sqlite-data-a; echo

# Now replace the instance: stop and delete A completely.
docker rm -f tf-sqlite-data-a

# Start a fresh instance (B) from the SAME image, attaching the SAME volume and database path.
docker run -d --name tf-sqlite-data-b -p 127.0.0.1:8083:8000 --mount type=volume,source=tf-sqlite-data,target=/var/lib/taskflow -e TASKFLOW_DB=/var/lib/taskflow/taskflow.db taskflow:4594076

# Give B a couple of seconds to start.
sleep 3

# Read the bookings on B. If the volume did its job, the booking is still here.
curl -s http://127.0.0.1:8083/tasks; echo

# Record instance B's full container id (evidence of the replacement instance).
docker inspect --format '{{.Id}}' tf-sqlite-data-b

# Record the image id B is running: same image as A confirms the replacement used the same build.
docker inspect --format '{{.Image}}' tf-sqlite-data-b

# Show B's mount: same volume source as A, proving it's a genuine replacement on shared storage.
docker inspect --format '{{json .Mounts}}' tf-sqlite-data-b; echo

# When you're finished, stop and remove B:
# docker rm -f tf-sqlite-data-b
