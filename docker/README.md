## Build
```sh
docker build -t lu0alv/task-tracker-app:python-server .
```

## Debug
```sh
CONFIG_FILE=${parent_dir}/task-service.conf
source $CONFIG_FILE
docker run -it --name task-service \
    -p ${task_service_port}:5554 \
    --env-file ${CONFIG_FILE} \
    --entrypoint /bin/bash \
    lu0alv/task-tracker-app:python-server -s
```

## Run
```sh
CONFIG_FILE=${parent_dir}/task-service.conf
source $CONFIG_FILE
docker run -it --name task-service \
    -p ${task_service_port}:5554 \
    --env-file ${CONFIG_FILE} \
    lu0alv/task-tracker-app:python-server
```
