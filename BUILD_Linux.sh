#!/bin/bash

pyinstaller -F ./main.py -i './img/icon.png' --hidden-import='tkinter' --hidden-import='PIL' --hidden-import='PIL._imagingtk' --hidden-import='PIL._tkinter_finder'
rm -r ./build
cp -r ./img ./dist
chmod +x ./dist/main
mv ./dist/main ./dist/DRichGen
mv ./dist './DiscordRichGenerator'
rm ./main.spec