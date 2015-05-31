#!/bin/sh
set -e

PYTHON_VERSION=3.4
PYTHON=python-$PYTHON_VERSION
PYVENV=pyvenv-$PYTHON_VERSION
PIP=pip3

MSA_DATA=/data
MSA_TMP=/data/.msa-tmp
MSA_DIST=$MSA_DATA/dist
MSA_DEPLOY=$MSA_DATA/deploy

# get application name
if [ ! -f "$MSA_DIST/.meta" ]; then
	echo "ERROR: $MSA_DIST/.meta does not exist."
	exit 1
fi
MSA_APP_NAME=`cat $MSA_DIST/.meta`

setup_pyvenv () {
	echo "Creating Python venv in $MSA_DEPLOY/env..."
	$PYVENV $MSA_DEPLOY/env
}

enter_pyvenv() {
	echo "Entering Python venv in $MSA_DEPLOY/env..."
	. $MSA_DEPLOY/env/bin/activate
}

install_python_packages () {
	if [ ! -d "$MSA_DIST/packages" ]; then
		echo "WARNING: $MSA_DIST/packages does not exist. No Python packages will be installed."
		return 0
	fi

	echo "Installing Python packages..."
	for PACKAGE in `ls $MSA_DIST/packages/`; do
		echo "Installing $PACKAGE..."
		$PIP install $MSA_DIST/packages/$PACKAGE
	done
}

copy_web_application () {
	if [ -d "$MSA_DEPLOY/$MSA_APP_NAME" ]; then
		echo "WARNING: $MSA_DEPLOY/$MSA_APP_NAME already exists. Skip copying web application from $MSA_DIST/$MSA_APP_NAME.tar.gz"
		return 0
	fi

	echo "Extracting $MSA_DIST/$MSA_APP_NAME.tar.gz to $MSA_TMP/"
	cd $MSA_TMP && tar zxvf $MSA_DIST/$MSA_APP_NAME.tar.gz
	echo "Moving $MSA_TMP/$MSA_APP_NAME to $MSA_DIST/$MSA_APP_NAME"
	mv $MSA_TMP/$MSA_APP_NAME $MSA_DEPLOY
}

setup () {
	mkdir -p $MSA_DEPLOY
	setup_pyvenv
	enter_pyvenv
	install_python_packages
	copy_web_application
}

if [ "$1" = "setup" ]; then
	echo "Setup api server."
	setup
	exec /bin/true
elif [ "$1" = "start" ]; then
	echo "Start api server."
	exec /bin/true
elif [ "$1" = "exec" ]; then
	shift
	echo "Exec $@."
	exec $@
else
	echo "ERROR: Cannot recognize task $@."
	echo "Usage: entrypoint.sh setup|exec"
	exit 1
fi

echo "ERROR: Should not see this message!"
exit 1
