#!/bin/bash

pyinstaller -F ./main.py -i './img/icon.png'
rm -r ./build
cp -r ./img ./dist
chmod +x ./dist/main
mv ./dist/main ./dist/DRichGen
mv ./dist './DiscordRichGenerator'
