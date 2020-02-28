#!/bin/sh

echo "Running bot. Press ctrl+c to quit"

now=$(date +"%H-%M-%S_%m_%d_%Y")
mkdir -p ./logs

# run until exit code 0; redirect all output to log.txt
until gunicorn --bind 0.0.0.0:8089 wsgi:app --access-logfile -  >> "logs/$now.log" 2>> "logs/$now.error" & echo $! > logs/pid ; do
    # if not exit code 0 output error to shell and restart
    now=$(date +"%H-%M-%S_%m_%d_%Y")
    echo "$now: Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
