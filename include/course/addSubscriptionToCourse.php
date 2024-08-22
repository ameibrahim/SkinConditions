<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];
    $courseID = $_POST['courseID'];
    $userID = $_POST['userID'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        INSERT INTO subscriptions (id, courseID, userID, status)
        VALUES ('$id', '$courseID', '$userID ', 'true')
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
