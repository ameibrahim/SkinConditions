<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];
    $title = $_POST['title'];
    $courseID = $_POST['courseID'];
    $hierarchy = $_POST['hierarchy'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        INSERT INTO lectures (id, title, courseID, hierarchy, done)
        VALUES ('$id', '$title', '$courseID', '$hierarchy', 'false')
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
