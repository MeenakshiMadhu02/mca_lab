#!/bin/bash
echo "Helloo  world!"
name="John"
echo "My name is $name"
read -p "Enter your age:"age
echo  "you are  $age years old."
if [  $age -ge  18];then
        echo "You are an adult."
else
        echo "You are a minor."
fi


