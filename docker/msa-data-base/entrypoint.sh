#!/bin/sh
set -e

MSA_TMP=$MSA_DATA/.msa-tmp
MSA_BACKUP=/backup

RUN_AS_MSA="gosu msa:msa"
EXEC_AS_MSA="exec $RUN_AS_MSA"

if [ "$1" = "start" ]; then
	echo "Start MSA data container."
	chown -R msa:msa $MSA_DATA
	$EXEC_AS_MSA /bin/true
elif [ "$1" = "copy" ]; then
	SRC_PATH=$2
	echo "Copy $SRC_PATH to $MSA_TMP."
	$RUN_AS_MSA mkdir -p $MSA_TMP
	$RUN_AS_MSA cp -a $SRC_PATH $MSA_TMP
	$EXEC_AS_MSA /bin/true
elif [ "$1" = "backup" ]; then
	echo "Backup $MSA_DATA to $MSA_BACKUP (ignoring $MSA_TMP)."
	$RUN_AS_MSA rm -rf $MSA_TMP
	$RUN_AS_MSA tar zcvf $MSA_BACKUP/backup-$(date +%F).tar.gz $MSA_DATA
	$EXEC_AS_MSA /bin/true
elif [ "$1" = "clean" ]; then
	echo "Clean $MSA_TMP."
	$RUN_AS_MSA rm -rf $MSA_TMP
	$EXEC_AS_MSA /bin/true
elif [ "$1" = "exec" ]; then
	shift
	echo "Exec $@."
	$EXEC_AS_MSA $@
elif [ "$1" = "sudo" ]; then
	shift
	echo "Sudo $@."
	exec $@
else
	echo "ERROR: Cannot recognize task $@."
	echo "Usage: entrypoint.sh start|copy|backup|clean|exec|sudo"
	exit 1
fi

echo "ERROR: Should not see this message!"
exit 1
