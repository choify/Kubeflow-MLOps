#!/bin/sh
cat ./data/titanic.csv.dvc | grep md5 | cut -d ' ' -f3 | cut -c -2 > prefix1.txt
cat ./data/titanic.csv.dvc | grep md5 | cut -d ' ' -f3 | cut -c 3- > prefix2.txt
sed -i "16c\\object_key = 'data/$(cat prefix1.txt)/$(cat prefix2.txt)'" train.py
rm ./prefix1.txt
rm ./prefix2.txt