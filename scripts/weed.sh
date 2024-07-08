#!/usr/bin/env bash

cd "$(dirname "$0")/.."

./bin/weed server \
  -dir=/data/weed \
  -master.port=9333 \
  -master.volumeSizeLimitMB=10000 \
  -volume.port=8080 \
  -volume.max=8 \
  -filer \
  -filer.port=8888