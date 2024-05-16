#!/bin/bash

set -eu

WORKER="$(pulp status | jq '.online_workers | map(select(.name | startswith("resource-manager") | not)) | length')"

# echo $'# TASKS\tDISPATCH_TIME\tPRIOR_TASKS\tTASK_GROUP\tAVG_COMPLETION\tWORKERS'

for i in $(seq 1 4)
do
  RESULT="$(http post http://localhost/pulp/api/v3/herminig/tasking_benchmark/ count=256 sleep_secs=0.5 resources_N=128 resources_K=2)"
  TASK_GROUP_HREF="$(echo "$RESULT" | jq -r '.task_group')"

  # Wait for taskgroup to finish
  TASK_GROUP="$(pulp task-group show --href "$TASK_GROUP_HREF")"
  while [ "$(echo "$TASK_GROUP" | jq '.waiting > 0 or .running > 0')" = "true" ]
  do
    sleep 2
    TASK_GROUP="$(pulp task-group show --href "$TASK_GROUP_HREF")"
  done

  AVG_SERVICE="$(echo "$TASK_GROUP" | \
    jq '.tasks | map({
      created: {c1: .pulp_created | [split(".")[0],"Z"] | join("") | fromdate | tostring, c2: .pulp_created | split(".")[1][:-1]} | values | join(".") | tonumber,
      started: {c1: .started_at | [split(".")[0],"Z"] | join("") | fromdate | tostring, c2: .finished_at | split(".")[1][:-1]} | values | join(".") | tonumber
    }) | map(.started - .created) | add / length')"

  AVG_COMPLETION="$(echo "$TASK_GROUP" | \
    jq '.tasks | map({
      created: {c1: .pulp_created | [split(".")[0],"Z"] | join("") | fromdate | tostring, c2: .pulp_created | split(".")[1][:-1]} | values | join(".") | tonumber,
      finished: {c1: .finished_at | [split(".")[0],"Z"] | join("") | fromdate | tostring, c2: .finished_at | split(".")[1][:-1]} | values | join(".") | tonumber
    }) | map(.finished - .created) | add / length')"

  echo "$(echo "$RESULT" | jq -r '[.[]]|@tsv')"$'\t'"$AVG_SERVICE"$'\t'"$AVG_COMPLETION"$'\t'"$WORKER"
done
