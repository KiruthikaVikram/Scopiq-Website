#!/bin/bash
# clear
# source /var/www/html/svn_scopiq/venv/bin/activate #Activate virtual environment
# cd /var/www/html/svn_scopiq  #path to your virtual environment
# python3 runserver.py localhost:$1 &

cd /var/www/html/svn_scopiq &&
python3 ./runserver.py


# echo $1
# echo $2
# exit 0


