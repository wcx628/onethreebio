#!/bin/bash
# Api template for getgene

for DRUG_ID in "$@"
do
curl "127.0.0.1:5000/api?=${DRUG_ID}"
done