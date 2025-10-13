#!/bin/bash
echo "Starting Student Snapshot Watcher"
echo ""
echo "Usage: ./start_snapshot_watcher.sh student_id [interval_seconds]"
echo "Example: ./start_snapshot_watcher.sh alice 10"
echo ""

if [ -z "$1" ]; then
    echo "ERROR: Please provide student_id"
    echo "Example: ./start_snapshot_watcher.sh alice"
    exit 1
fi

STUDENT_ID=$1
INTERVAL=${2:-10}

echo "Watching code changes for: $STUDENT_ID"
echo "Snapshot interval: $INTERVAL seconds"
echo ""
echo "Press Ctrl+C to stop watching"
echo ""

python3 watch_student_changes.py $STUDENT_ID $INTERVAL

