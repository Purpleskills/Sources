#!/bin/bash

if [[ $1 ]] && [[ $2 ]]; then
    echo "Source: " $1
    echo "Destination: " $2
    cp -r $1/psweb $2/psweb
    cp -r $1/learn $2/learn
    cp -r $1/.ebextensions $2/.ebextensions
    cp -r $1/manage.py $2/manage.py
    cp -r $1/requirements.txt $2/requirements.txt

    find $2 -type f -name "*.pyc" -exec rm -f {} \;
    find $2 -type f -name "*.*~" -exec rm -f {} \;
    find $2 -type d -name "migrations" -exec rm -rf {} \;
    find $2 -type d -name "media" -exec rm -rf {} \;
fi
