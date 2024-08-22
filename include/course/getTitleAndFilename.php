<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $courseID = $_POST["id"];

    $query = "
        SELECT title, filename FROM courses
        INNER JOIN objectives ON objectives.courseID = courses.id
        WHERE courses.id = '$courseID'
    ";

    $detailsResult = mysqli_query($conn,$query);
    $details = mysqli_fetch_all($detailsResult,MYSQLI_ASSOC);

    echo json_encode($details);
