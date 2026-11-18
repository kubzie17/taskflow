# Optional host, port and volume inspection
Use only a personal or designated training machine. This experiment answers whether the running image contains the booking access controls, and whether the gateway points to the service you believe it does. All core challenges also run in Python.
1. From the repo root examine `Get-Content .\Dockerfile` and `docker version`. If there is no Dockerfile, daemon or approved image source, use the historical configuration exhibit in the evidence sheet and the live Python gateway. Do not substitute arbitrary images.
2. Use a unique disposable name. Keep this PowerShell terminal open so the variables survive. Run each line separately and stop on a Docker error. A local build can download packages and the base image.
```powershell
$suffix = [guid]::NewGuid().ToString('N').Substring(0,8)
$containerName = "tf7-container-$suffix"
$volumeName = "tf7-volume-$suffix"
$imageName = "taskflow:day7-$suffix"
docker build -t $imageName .
docker volume create $volumeName
docker run -d --name $containerName --publish 127.0.0.1:8073:8000 --mount "type=volume,source=$volumeName,target=/var/lib/taskflow" $imageName
docker port $containerName
docker inspect --format '{{json .Config.Cmd}}' $containerName
docker inspect --format '{{json .Mounts}}' $containerName
docker inspect --format '{{json .NetworkSettings.Ports}}' $containerName
```
3. Compare direct `http://127.0.0.1:8073/health` and gateway: `python -m exercises.day07_lab point 8073` then `python -m exercises.day07_lab call health`. Use only a fictional title: `python -m exercises.day07_lab call book --title "Container entry probe"`. Record observed response and runtime. If you see a change of auth behaviour, compare entry point and files copied. Do not send Friday credentials to an unverified container.
4. Point back to your verified Python service: `python -m exercises.day07_lab point 8071`. Recheck `python -m exercises.day07_lab call health`. Save the previous results before removal.
5. Cleanup only resources you created above. Remove the disposable volume only when its fictional work is no longer needed. Confirm container/volume lists filtered to the exact generated names show no entries. If a build or launch failed, inspect each name first and clean up the items actually created.
```powershell
docker rm -f $containerName
docker volume rm $volumeName
docker image rm $imageName
docker ps -a --filter "name=$containerName"
docker volume ls --filter "name=$volumeName"
```
