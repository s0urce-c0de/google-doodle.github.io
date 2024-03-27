#!/bin/bash
for doodle in $(jq -r '.[]' doodles/doodles.json); do
  git remote remove "$doodle" 
done