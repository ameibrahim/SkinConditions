<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];
    $lectureID = $_POST['lectureID'];
    $courseID = $_POST['courseID'];
    $name = $_POST['name'];
    $dateGenerated = $_POST['dateGenerated'];
    $filename = $_POST['filename'];
    $totalMarks = $_POST['totalMarks'];


    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        INSERT INTO quiz (id, name, courseID, lectureID, dateGenerated, filename, totalMarks)
        VALUES ('$id', '$name', '$courseID', '$lectureID', '$dateGenerated', '$filename', '$totalMarks')
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
