#!/usr/bin/env bash

cd "$(dirname "$0")/.."

./core/seaweedfs/weed server -master.port=9333 -volume.port=8080 -dir=/data/weed