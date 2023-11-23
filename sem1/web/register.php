<?php
if($_SERVER["REQUEST_METHOD"]=="POST"){
    $name=$_POST["name"];
    $email=$_POST["email"];
    $password=$_POST["password"];
    $confirmPassword=$_POST["confirm_password"];
    if($password !== $confirmPassword){
      echo "Passwords do not match.Please try again.";
    }else{
      if(strlen($password) < 6){
         echo "Password must be atleast 6 characters long.";
      }else{
         echo "Registration successful!Welcome,".$name."!";
      }
   }
}
?>
