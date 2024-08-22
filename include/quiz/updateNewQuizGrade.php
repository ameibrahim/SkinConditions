<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();


    $id = $_POST['id'];
    $userID = $_POST['userID'];
    $quizID = $_POST['quizID'];
    $filename = $_POST['filename'];
    $status = $_POST['status'];
    $value = $_POST['value'];
    $timeEnded = $_POST['timeEnded'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        UPDATE quizGrades
        SET filename='$filename', status = '$status', timeEnded = '$timeEnded',
        value = '$value', quizID = '$quizID', userID = '$userID'
        WHERE id='$id'
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
