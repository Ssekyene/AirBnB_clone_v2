#!/usr/bin/env bash
#deploys webstatic
fab -f 1-pack_web_static.py do_pack

archive=$(ls -t versions/ | head -n 1)
if [ -z $archive ]; then
    echo "Archive not found in version directory."
    exit 1
fi

fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/$archive \
-i ~/.ssh/school -u ubuntu
if [ $? -ne 0 ]; then
    echo "Deployment Failed."
else
    echo "Depoloyment Successful"
fi
