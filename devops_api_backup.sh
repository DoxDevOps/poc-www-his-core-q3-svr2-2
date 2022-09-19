#!/bin/bash --login
echo "--------------------------------------------"
echo "Changing directory to API-log"
echo "--------------------------------------------"
cd /var/www/BHT-EMR-API/log
echo "--------------------------------------------"
echo "Removing log file"
echo "--------------------------------------------"
rm -rf development.log
echo "____________________________________________"
echo "Changing directory to www"
echo "____________________________________________"
cd ../..
echo "____________________________________________"
echo "Backing up API folder"
echo "____________________________________________"
scp -Cr BHT-EMR-API BHT-EMR-API-DEV-BK
echo "____________________________________________"
