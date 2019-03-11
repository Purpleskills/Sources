#!/bin/bash

if [[ $1 ]] && [[ $2 ]]; then
    echo "Source: " $1
    echo "Destination: " $2
    cp -r $1/psweb $2/psweb
    cp -r $1/learn $2/learn
    cp -r $1/contentprovider $2/contentprovider
    cp -r $1/core $2/core
    cp -r $1/home $2/home
    cp -r $1/media $2/media
    cp -r $1/mgmt $2/mgmt
    cp -r $1/psauth $2/psauth
    cp -r $1/.ebextensions $2/.ebextensions
    cp -r $1/manage.py $2/manage.py
    cp -r $1/requirements.txt $2/requirements.txt
    touch $2/purpleskills.log
    chmod 777 $2/purpleskills.log
    touch $2/provider.log
    chmod 777 $2/provider.log
    mkdir $2/contentprovider/nltk_data
    chmod 777 $2/contentprovider/nltk_data


    find $2 -type f -name "*.pyc" -exec rm -f {} \;
    find $2 -type f -name "*.*~" -exec rm -f {} \;
    find $2 -type d -name "migrations" -exec rm -rf {} \;
    find $2 -type d -name "media-temp" -exec rm -rf {} \;
    find $2 -type d -name "img-temp" -exec rm -rf {} \;
fi
