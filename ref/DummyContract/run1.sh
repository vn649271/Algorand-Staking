#!/usr/bin/env bash

phrase=$1
to_address=$2
#echo $to_address
#echo "##########################################"
#sha256sumed=`python3 phrase2sha256.py ${phrase}`
base64ed_with_spaces=`echo -n "${phrase}" | base64`
base64ed=`echo $base64ed_with_spaces | sed 's/ //g'`
#echo "base64=${base64ed}"
app_address=`goal clerk compile sample1.teal | awk -F': ' '{print $2}'`
#echo $app_address
escrow_balance=`goal account balance -a $app_address -d /var/lib/algorand_testnet`
escrow_balance=`echo $escrow_balance | awk -F' ' '{print $1}'`
echo $escrow_balance
if [ $((escrow_balance - 0)) -eq 0 ]; then
    echo "Fund into '${app_address}' before run this script"
    exit
fi
#echo $to_address
#echo $base64ed
goal clerk send -a 3000 --from-program sample1.teal  -c $to_address --argb64 $base64ed -t $to_address -o out1.txn -d /var/lib/algorand_testnet
goal clerk rawsend -f out1.txn -d /var/lib/algorand_testnet
goal account balance -a  $app_address -d /var/lib/algorand_testnet

