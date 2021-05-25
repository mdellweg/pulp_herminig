#!/bin/bash

set -eu

WORKER="$(pulp status| jq '.online_workers | map(select(.name | startswith("resource-manager") | not)) | length')"

for i in $(seq 1 8)
do
  RESULT="$(http post localhost/pulp/api/v3/herminig/tasking_benchmark count="$((2**$i))")"
  TASK_GROUP_HREF="$(echo $RESULT | jq -r '.task_group')"

  # Wait for taskgroup to finish
  TASK_GROUP="$(pulp task-group show --href "$TASK_GROUP_HREF")"
  while [ "$(echo "$TASK_GROUP" | jq '.waiting > 0 or .running > 0')" = "true" ]
  do
    sleep 2
    TASK_GROUP="$(pulp task-group show --href "$TASK_GROUP_HREF")"
  done

  AVG_COMPLETION="$(echo "$TASK_GROUP" | \
    jq '.tasks | map({
      created: {c1: .pulp_created | [split(".")[0],"Z"] | join("") | fromdate | tostring, c2: .pulp_created | split(".")[1][:-1]} | values | join(".") | tonumber,
      finished: {c1: .finished_at | [split(".")[0],"Z"] | join("") | fromdate | tostring, c2: .finished_at | split(".")[1][:-1]} | values | join(".") | tonumber
    }) | map(.finished - .created) | add / length')"

  echo "$(echo "$RESULT" | jq -r '[.[]]|@tsv')"$'\t'"$AVG_COMPLETION"$'\t'"$WORKER"
done
