FROM lu0alv/git-partial-clone:latest

ENV TZ=America/Monterrey
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update
RUN apt install -y tzdata

RUN apt install -y python3 python3-pip

ENTRYPOINT ["/bin/sh", "-c" , "get-source && /home/${PARENT_DIR}/${REPO_NAME}/${REMOTE_PARTIAL_DIR}/deploy.sh"]
