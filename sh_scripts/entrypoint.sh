#!/bin/sh
rm -f /tmp/*.pid
exec "$@"
