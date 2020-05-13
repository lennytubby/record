#!/bin/bash
#
# 1 - Subject
# 2 - Body
# 3 - Mail Adress
`printf "Subject: "$1"\n\n"$2 | ssmtp $3`
# installed ssmto
# editied /etc/ssmtp/ssmtp.conf to:
#  FromLineOverride=YES
#  UseSTARTTLS=YES
#  FromLineOverride=YES
#  root=lennytubby.server@gmail.com
#  mailhub=smtp.gmail.com:587
#  AuthUser=lennytubby.server@gmail.com
#  AuthPass=HabTassiaLieb1

