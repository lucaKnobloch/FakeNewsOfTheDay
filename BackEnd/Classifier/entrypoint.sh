#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/app/container.env
APP = /app/
10 0 * * * echo "Job has been started" >> /var/log/load.log 2>&1
10 0 * * * python3 loadFromElastic.py >> /var/log/load.log 2>&1 sleep 30
20 0 * * * echo "Job has been started" >> /var/log/classify.log 2>&1 sleep 120
20 0 * * * python3 classifier.py >> /var/log/classify.log 2>&1 sleep 120
45 0 * * * echo "Job has been started" >> /var/log/push.log 2>&1 sleep 30
45 0 * * * python3 pushToElastic.py >> /var/log/push.log 2>&1 sleep 30
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
