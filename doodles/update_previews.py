#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import re
import json
import shutil
import pathlib
import requests

path = pathlib.Path(__file__).parent.resolve()

os.chdir(path)

# delete alteady made folder
os.makedirs("previews", mode=0o755, exist_ok=True)
os.rename("previews", ".previews.bak")
try:
  # make the directory
  os.makedirs("previews/image-title", mode=0o755, exist_ok=True)
  os.makedirs("previews/images", mode=0o755, exist_ok=True)
  os.makedirs("previews/all-images", mode=0o755, exist_ok=True)

  images={}

  with open(path / "images.json") as images_json:
    images=json.load(images_json)

  os.chdir( path / "previews" / "all-images" )

  image_extensions=["png", "apng", "gif", "jpg", "jpeg", "jfif",
                    "pjpeg", "pjp", "tif", "tiff", "bmp", "raw",
                    "avif", "svg", "webp"]
  # censor the extensions
  for i in range(len(image_extensions)):
    image_extensions[i] = image_extensions[i].replace("/", "")
    image_extensions[i] = re.escape(image_extensions[i])
  image_regex=f"^.*\.(?:{'|'.join(image_extensions)})$"

  for key in images.keys():
    if key!="main":
      for image_url in images[key].values():
        image_name=image_url.split("/")[-1]
        img = requests.get(image_url)
        # if not an image add an image extension
        if not re.match(image_regex, image_name):
          if img.headers.get('Content-Type', "text/plain").split(";")[0].split("/")[0]=="image":
            image_name += "."+img.headers.get('Content-Type', "text/plain").split(";")[0].split("/")[-1].replace("svg+xml", "svg")
          else:
            pass # i couldn't care less
        with open(image_name, "wb") as image:
          image.write(img.content)

  os.chdir(path / "previews" / "image-title" )

  for key in images.keys():
    if key!="main":
      for image_name, image_url in images[key].items():
        image_name=image_name.split("/")[-1]
        img = requests.get(image_url)
        # if not an image add an image extension
        if not re.match(image_regex, image_name):
          if img.headers.get('Content-Type', "text/plain").split(";")[0].split("/")[0]=="image":
            image_name += "."+img.headers.get('Content-Type', "text/plain").split(";")[0].split("/")[-1]
          else:
            pass # i couldn't care less
        with open(image_name, "wb") as image:
          image.write(img.content)

  os.chdir(path / "previews" / "images" )

  images_per_doodle = {}
  for doodle, image_index in images["main"].items():
    image_name = doodle
    image_url = images[doodle][image_index]
    img = requests.get(image_url)
    if re.match(image_regex, image_url.split("/")[-1]):
      image_name += "." + image_url.split("/")[-1].split(".")[-1]
    else:
      if img.headers.get('Content-Type', "text/plain").split(";")[0].split("/")[0]=="image":
        image_name += "."+img.headers.get('Content-Type', "text/plain").split(";")[0].split("/")[-1]
      else:
        pass # just leave it
    images_per_doodle[doodle] = image_name
    with open(image_name, "wb") as image:
      image.write(img.content)
  try:
    os.chdir(path)
    shutil.rmtree(".previews.bak")
  except FileNotFoundError as error:
    raise error
  os.chdir(path)
except BaseException as e:
  # See https://docs.python.org/3/library/exceptions.html#exception-hierarchy
  # to see why I am catching BaseException, not Exception
  os.chdir(path)
  shutil.rmtree("previews")
  os.rename(".previews.bak", "previews")
  raise e

with open("images-per-doodle.json", "wt") as file:
  json.dump(images_per_doodle, file, sort_keys=True, indent=2)