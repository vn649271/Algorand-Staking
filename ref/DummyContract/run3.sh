#!/usr/bin/env bash

app_address=`goal clerk compile sample3.teal | awk -F': ' '{print $2}'`
echo $app_address
echo "-------------------------------------------------------"
goal account balance -a $app_address -d /var/lib/algorand_testnet

#goal clerk compile sample2.teal 
#goal account balance -a  RZ2CUMV2VG3NCVFEVUVHVBYQUABQIBWAT3AC736Y6YL7PPDNAD7K3TVNAI -d /var/lib/algorand_testnet
goal clerk send -a 30000 --from-program sample3.teal  -c GHO5CRXK575LJEO7EALG76KSQZXU7HF3AD27NK2TGMPZWMF7SZUNNU7RTU --argb64 WjVMa09GU1BDbjZnTFV6a3VCYmt6TTYvUjNQQ3NQcXRyNG1vQ3pGUm45ND0K -t GHO5CRXK575LJEO7EALG76KSQZXU7HF3AD27NK2TGMPZWMF7SZUNNU7RTU -o out.txn -d /var/lib/algorand_testnet
goal clerk rawsend -f out.txn -d /var/lib/algorand_testnet
goal account balance -a $app_address -d /var/lib/algorand_testnet



