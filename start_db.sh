#!/usr/bin/env bash

DIR=$(cd "$(dirname "$0")"; pwd)

docker run \
--detach \
--user neo4j \
--publish=80:7474 \
--publish=443:7473 \
--publish=7687:7687 \
--volume=$DIR/neo4j/input:/input \
-e NEO4J_AUTH=none \
-e NEO4J_dbms_read__only=true \
-e EXTENSION_SCRIPT=/input/extension_script.sh \
neo4j