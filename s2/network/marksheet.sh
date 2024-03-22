
echo "Student Marksheet"

echo "Enter OS Marks:"
read os
echo "Enter C++ Marks:"
read cpp
echo "Enter Java Marks:"
read java

total=`expr $os + $cpp + $java`
echo "Total Marks:"$total

if [ $total -ge 110 ]
then
echo "Grade A"
elif [ $total -ge 70 ]
then
echo "Grade B"
elif [ $total -ge 40 ]
then
echo "Grade c"
else
echo "Class: Fail"
fi

