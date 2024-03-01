#!/bin/bash
echo "Enter the year"
read n
num=$(( $n % 4 ))
if [ $num -eq 0 ]
then
 echo "It is leap year"
else
 echo "Not a leap year"
fi
