#!/bin/bash

cd "$(dirname "$(dirname "$0")")"

for doodle in $(jq -r '.[]' doodles/doodles.json); do
  git remote remove "$doodle" 
done