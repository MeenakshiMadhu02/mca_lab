<?php
$db=new mysqli("localhost","username","password","database_name");
if($db->connect_error){
 die("Connection failed:".$db->connect_error);
}
else{
 echo "Connection established";
}
$result=$db->query("SELECT * FROM users");
while($row=$result->fetch_assoc()){
 echo "Name:".$row['name']."<br>";
}
$db->close();
?>
