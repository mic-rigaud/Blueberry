# @Author: michael
# @Date:   23-Jun-2019
# @Filename: sendEvent.sh
# @Last modified by:   michael
# @Last modified time: 23-Jun-2019
# @License: GNU GPL v3
#!/bin/sh



TOKEN="{{token}}"
CHAT_ID="{{chat_id}}"

ACTION=$1
USER=$2
IP=$3
ALERTID=$4
RULEID=$5

LOCAL=`dirname $0`;
cd $LOCAL
cd ../
PWD=`pwd`


# Logging the call
echo "`date` $0 $1 $2 $3 $4 $5 $6 $7 $8" >> ${PWD}/../logs/active-responses.log


# Getting alert time
ALERTTIME=`echo "$ALERTID" | cut -d  "." -f 1`

# Getting end of alert
ALERTLAST=`echo "$ALERTID" | cut -d  "." -f 2`

# Getting full alert
ALERT=`grep -A 5 "$ALERTTIME" ${PWD}/../logs/alerts/alerts.log | grep -v ".$ALERTLAST: " -A 5`

curl -s \
-X POST \
https://api.telegram.org/bot$TOKEN/sendMessage \
-d text="$ALERT" \
-d chat_id=$CHAT_ID
