<?php

    include "databaseConnection.php"; 

    $conn = OpenConnection();

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    // For users table
    $id = $_POST['id'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    $role = $_POST['role'];
    $timestamp = $_POST['timestamp'];

    $name = $_POST['name'];
    $address = $_POST['address']; // should be optional
    $image = $_POST['image']; // should be optional
    $phone = $_POST['phone']; // should be optional
    $institutionID = $_POST['institutionID'];
    $department = $_POST['department'];

    $queryUserDetails = "
    INSERT INTO `userDetails`(`id`, `name`, `address`, `image`, `phone`, `institutionID`, `department`) VALUES ('$id','$name','$address','$image','$phone','$institutionID','$department')
    ";

    $queryUsers = "
    INSERT INTO `users`(`id`, `email`, `password`, `role`, `timestamp`) VALUES ('$id','$email','$password','$role','$timestamp')
    ";

    $resultA = mysqli_query($conn,$queryUserDetails);
    $resultB = mysqli_query($conn,$queryUsers);

    if($resultA && $resultB) echo "success";
    // echo "$id+$email+$password+$role+$timestamp\n";
    // echo "$name+$address+$image+$phone+$institutionID+$department";
