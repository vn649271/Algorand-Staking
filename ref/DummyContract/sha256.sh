#!/usr/bin/env bash

phrase=$1
sha256sumed=`python3 phrase2sha256.py ${phrase}`
echo $sha256sumed
sha256_len=${#sha256sum}
echo "passphrase length: ${sha256_len}"
echo "sha256 of passphrase: ${sha256sumed}"
