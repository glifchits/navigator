#!/usr/bin/env bash

oldwd=$(pwd)
cd ~/Development/navigator
echo 'Retrieving latest job application info, please wait...'
python navigator_text.py
if [ $? -ne 0 ]; then
  exit $?
fi

FIRSTTODAY=$(ls | grep `date +%Y-%m-%d` | sort | head -n 1)
SECOND=$(ls | grep '^2014.*.csv$' | sort | tail -n 2 | head -n 1)
LAST=$(ls | grep '^2014.*.csv$' | sort | tail -n 1)
cmp=$(diff $SECOND $LAST)
cmptoday=$(diff $FIRSTTODAY $LAST)

if [ "$cmp" == '' ]; then
  echo "No changes since last checked."
else
  echo "$cmp" | less
fi

if [ "$cmptoday" = '' ]; then
  echo "There has been no change in job application status today."
elif [ "$1" = '' ]; then
  echo "You are about to see all jobs with changed status today."
  read -t 4 
  echo "$cmptoday" | less
fi


cd $oldwd
