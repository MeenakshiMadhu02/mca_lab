<?php
$students = array(
"John",
"Alice",
"Bob",
"Charlie",
"Eve"
);
echo "Original array:\n";
print_r($students);

asort($students);
echo "\nSorted array in ascending order:\n";
print_r($students);

arsort($students);
echo "\nSorted array in descending order:\n";
print_r($students);
?>

