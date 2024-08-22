<?php

    include "databaseConnection.php"; 


    $conn = OpenConnection();

    $id = $_POST['id'];
    $image = $_POST['image'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        UPDATE userDetails
        SET image='$image'
        WHERE id='$id'
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
