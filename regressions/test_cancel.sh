#!/bin/bash

set -eu

# pulp --refresh-api status

for _ in $(seq 1000)
do
  task_group="$(pulp debug tasking-test --count 2 --sleep-secs 15 | jq -r '.task_group')"
  tasks=$(pulp task-group show --href "$task_group" | jq -r '.tasks[].pulp_href')

  for task in $tasks
  do
    pulp --background task cancel --href "$task" >/dev/null 2>&1 || true
  done
  for task in $tasks
  do
    task_state=$(pulp task show --wait --href "$task" | jq -r '.state')
    [ "$task_state" = "canceled" ] || echo "$task_state"
  done

done
echo "Made it to the end..."
