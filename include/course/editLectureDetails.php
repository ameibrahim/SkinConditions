<?php

    include "../databaseConnection.php"; 


    $conn = OpenConnection();

    $lectureID = $_POST['lectureID'];
    $title = $_POST['title'];
    $hierarchy = $_POST['hierarchy'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        UPDATE lectures
        SET title='$title', hierarchy='$hierarchy'
        WHERE id='$lectureID'
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
