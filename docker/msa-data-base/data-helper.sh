#!/bin/sh
set -e

DATA_IMAGE_NAME=msa/data-base
DATA_CONTAINER_NAME=msa-data-example
TMP_CONTAINER_NAME=$DATA_CONTAINER_NAME-tmp

if [ "$1" = "start" ]; then
	sudo docker run -d --name $DATA_CONTAINER_NAME $DATA_IMAGE_NAME start
	exit 0

elif [ "$1" = "copy" ]; then
	SRC_PATH=$2
	if [[ "$SRC_PATH" != /* ]]; then
		SRC_PATH=`pwd`/$SRC_PATH
	fi

	MOUNT_POINT=/`basename $SRC_PATH`
	sudo docker run -it --name $TMP_CONTAINER_NAME \
		--volumes-from $DATA_CONTAINER_NAME \
		-v $SRC_PATH:$MOUNT_POINT \
		$DATA_IMAGE_NAME \
		copy $MOUNT_POINT
	sudo docker rm -v $TMP_CONTAINER_NAME

elif [ "$1" = "backup" ]; then
	DEST_PATH=$2
	if [ ! -d "$DEST_PATH" ]; then
		echo "Backup path must be a directory."
		exit 1
	fi

	if [[ "$DEST_PATH" != /* ]]; then
		DEST_PATH=`pwd`/$DEST_PATH
	fi

	MOUNT_POINT=/backup
	sudo docker run -it --name $TMP_CONTAINER_NAME \
		--volumes-from $DATA_CONTAINER_NAME \
		-v $DEST_PATH:$MOUNT_POINT \
		$DATA_IMAGE_NAME \
		backup
	sudo docker rm -v $TMP_CONTAINER_NAME

elif [ "$1" = "clean" ]; then
	sudo docker run -it --name $TMP_CONTAINER_NAME \
		--volumes-from $DATA_CONTAINER_NAME \
		$DATA_IMAGE_NAME \
		clean
	sudo docker rm -v $TMP_CONTAINER_NAME

elif [ "$1" = "exec" ]; then
	shift
	sudo docker run -it --name $TMP_CONTAINER_NAME \
		--volumes-from $DATA_CONTAINER_NAME \
		$DATA_IMAGE_NAME \
		exec $@
	sudo docker rm -v $TMP_CONTAINER_NAME

elif [ "$1" = "shell" ]; then
	sudo docker run -it --name $TMP_CONTAINER_NAME \
		--volumes-from $DATA_CONTAINER_NAME \
		$DATA_IMAGE_NAME \
		exec /bin/bash
	sudo docker rm $TMP_CONTAINER_NAME

elif [ "$1" = "clean-docker" ]; then
	sudo docker rm -f -v $TMP_CONTAINER_NAME

else
	echo "Usage: $0 start|copy|backup|clean|exec|shell|clean-docker"
	exit 1
fi

exit 0
