# Challenge 2 — Getting Started with Docker Volumes

## The problem

You've successfully packaged TaskFlow and run it inside a Docker container.

However, when a container is removed, data stored only in that container's writable layer is lost.

**Your challenge is to ensure that SQLite booking data survives when the container is removed and replaced.**

## 1. Consider Docker volumes

Docker provides **volumes**, which allow data to be stored independently of an individual container.

Think of a volume as a separate storage location that a container can access.

A container can be removed without automatically deleting its named volume. Another container can then use the same volume.

Useful commands to explore:

```powershell
# Create a named volume
docker volume create my-data

# List existing volumes
docker volume ls

# Inspect a specific volume
docker volume inspect my-data
```

Try creating your own appropriately named volume for TaskFlow.

## 2. How do you connect a volume to a container?

Docker allows you to attach a volume when creating a container using either `-v` or `--mount`.

For example, the general structure is:

```text
--mount type=volume,source=VOLUME_NAME,target=CONTAINER_DIRECTORY
```

- `source` identifies the Docker volume.
- `target` identifies where that volume will be accessible inside the container.

You can include this option in a `docker run` command.

**Your investigation:** Where should the volume be mounted so that TaskFlow can store its SQLite database inside it?

## 3. Check TaskFlow's database configuration

Inspect the project's `app/database.py` and `app/main.py`.

TaskFlow normally stores its database at:

```text
data/taskflow.db
```

It also supports an environment variable:

```text
TASKFLOW_DB
```

Remember that Docker allows environment variables to be supplied when starting a container.

**Questions to investigate:**

1. How can you tell TaskFlow to save its database in a different location?
2. How could you make that location part of your mounted volume?
3. What would happen if the volume were mounted at one directory, but SQLite wrote somewhere else?

## 4. Test your solution

Once you've configured your volume:

1. Start Container A using your persistent storage.
2. Create one booking and record its ID.
3. Stop and remove Container A.
4. Start Container B using the same image and storage.
5. Use `GET /tasks` to find the original booking.

Remember: **You must not create the booking again after replacing the container.**

## 5. Prove it worked

Your evidence must demonstrate that:

- Container A and Container B have different IDs.
- Both containers use the same image.
- Both use the intended persistent storage.
- The original booking ID and title remain unchanged.

Useful investigation commands:

```powershell
docker ps -a
docker volume ls
docker volume inspect VOLUME_NAME
docker inspect CONTAINER_NAME
docker logs CONTAINER_NAME
```

**Further reading:** [Docker's official guide to volumes](https://docs.docker.com/engine/storage/volumes/)

### Stretch challenge

Can you make a replacement container return HTTP 200 from `/health` while the original booking is missing?

Investigate why this happens and how you could recover the booking without creating it again.

**Important:** Do not delete the volume containing your original booking.
