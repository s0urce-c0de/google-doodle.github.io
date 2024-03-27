#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import json
import pathlib

path = pathlib.Path(__file__).parent.resolve()

os.chdir(path)

with open("doodles.json") as doodles_json, \
     open("names.json") as names_json, \
     open("summaries.json") as summaries_json, \
     open("images-per-doodle.json") as images_per_doodle_json:
  doodles_list = set(json.load(doodles_json))
  names = json.load(names_json)
  summaries = json.load(summaries_json)
  images_per_doodle = json.load(images_per_doodle_json)

# use sets so that the keys can be in any order
# and are stored in the same manner
assert set(doodles_list)==set(names.keys()) \
                        ==set(summaries.keys()) \
                        ==set(images_per_doodle.keys()), \
f"Names or Summaries seem to be not properly updated. \n\
Doodles List:\n\
{json.dumps(doodles_list, indent=2)}\n\
Summaries JSON:\n\
{json.dumps(summaries, indent=2)}\n\
Names JSON: \n\
{json.dumps(names, indent=2)}"

doodles = {}

for i in doodles_list:
  doodles[i] = {
    "name": names[i],
    "preview-image": images_per_doodle[i],
    "summary": summaries[i] 
  }

with open("doodle.json", "wt") as out:
  json.dump(doodles, out, sort_keys=True, indent=2)