<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $userID = $_POST['userID'];
    $quizID = $_POST['quizID'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
    SELECT *
    FROM `quizGrades`
    WHERE userID='$userID' && quizID='$quizID'
    ";

    $quizGradeResults = mysqli_query($conn,$query);
    $grades = mysqli_fetch_all($quizGradeResults,MYSQLI_ASSOC);

    echo json_encode($grades);

