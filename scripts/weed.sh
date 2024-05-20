#!/usr/bin/env bash

cd "$(dirname "$0")/.."

./core/seaweedfs/weed server \
  -master.port=9333 \
  -master.volumeSizeLimitMB=29999 \
  -volume.port=8080 \
  -volume.max=8 \
  -filer \
  -filer.port=8888
  -dir=/data/weed