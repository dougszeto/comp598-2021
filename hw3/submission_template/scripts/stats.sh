#!/bin/bash
if [ $(wc -l < $1) -lt 10000 ]
then
	echo "The input file must be larger than 10,000 lines"
	return 1
fi
wc -l < $1
head -n 1 $1
tail -n 10000 $1 | grep -c -i "potus"
head -n 200 $1 | tail -n 100 | grep -c "fake"
