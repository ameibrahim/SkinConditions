<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];
    $courseID = $_POST['courseID'];
    $filename = $_POST['filename'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        INSERT INTO objectives (id, courseID, filename)
        VALUES ('$id', '$courseID', '$filename')
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
