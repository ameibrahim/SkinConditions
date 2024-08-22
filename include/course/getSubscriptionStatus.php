<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];
    $userID = $_POST['userID'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        SELECT status FROM `subscriptions`
        INNER JOIN courses ON courses.id = subscriptions.courseID
        WHERE subscriptions.userID = '$userID' AND subscriptions.courseID = '$id'
    ";

    $coursesResult = mysqli_query($conn,$query);
    $courses = mysqli_fetch_all($coursesResult,MYSQLI_ASSOC);

    echo json_encode($courses);

