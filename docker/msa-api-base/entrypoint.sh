#!/bin/sh
set -e

exec gosu msa:msa /msa-entrypoint.sh $@
