#!/bin/sh
python render_all_notebooks.py
dos2unix content/post/2018-05-10-seinfeld_effect.md
hugo
git add . && git commit -m "update" && git push
cd adelr.github.io && git add . && git commit -m "update" && git push
cd ..
