#!/bin/bash
echo "Enter the string"
read s
echo $s>temp
reverse="$(rev temp)"
echo "Reversed string is :"$reverse
if [ $s = $reverse ]
then
echo "It is palindrome"
else
echo "It is not palindrome"
fi
