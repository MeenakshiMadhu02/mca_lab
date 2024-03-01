#!/bin/bash
echo "Enter the number"
read n
for((i=2; i<=n/2; i++))
do
 num=$(( n%i ))
 if [ $num -eq 0 ]
 then
  echo "$n is not prime"
  exit 0
 fi
done
echo "$n is a prime number"
