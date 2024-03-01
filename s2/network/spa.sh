#!/bin/bash
echo "Enter first number"
read a
echo "Enter second number"
read b
echo "Enter third number"
read c
echo "Enter fourth number"
read d
s=$(( $a + $b + $c + $d ))
p=$(( $a * $b * $c * $d ))
a=$(( $s / 4 ))
echo "Sum="$s
echo "Product="$p
echo "Average="$a
