#!/usr/bin/env bash

goal clerk compile sample2.teal 
goal account balance -a  RZ2CUMV2VG3NCVFEVUVHVBYQUABQIBWAT3AC736Y6YL7PPDNAD7K3TVNAI -d /var/lib/algorand_testnet
goal clerk send -a 30000 --from-program sample2.teal  -c STF6TH6PKINM4CDIQHNSC7QEA4DM5OJKKSACAPWGTG776NWSQOMAYVGOQE --argb64 d2VhdGhlciBjb21mb3J0IGVydXB0IHZlcmIgcGV0IHJhbmdlIGVuZG9yc2UgZXhoaWJpdCB0cmVlIGJydXNoIGNyYW5lIG1hbg==  -t STF6TH6PKINM4CDIQHNSC7QEA4DM5OJKKSACAPWGTG776NWSQOMAYVGOQE -o out.txn -d /var/lib/algorand_testnet
goal clerk rawsend -f out.txn -d /var/lib/algorand_testnet
goal account balance -a  RZ2CUMV2VG3NCVFEVUVHVBYQUABQIBWAT3AC736Y6YL7PPDNAD7K3TVNAI -d /var/lib/algorand_testnet



