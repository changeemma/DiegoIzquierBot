#!/bin/bash
pushd "$(dirname "$0")"

# Telegram Bot
./boton.py &

# Doris Camera Monitor
./dorimon.py &

# SCPC Gateway Monitor
./gatomon-scpcgw.py &

# ARSAT Gateway Monitor
./gatomon-wangw.py &

popd

