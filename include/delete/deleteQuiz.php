<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        SELECT filename
        FROM `quiz`
        WHERE id='$id'
    ";

    $quizzesQuery = mysqli_query($conn,$query);
    $quizzes = mysqli_fetch_all($quizzesQuery,MYSQLI_ASSOC);

    $deleteQuery = "
    DELETE FROM `quiz`
    WHERE id='$id'
    ";

    $deleteQueryResponse = mysqli_query($conn,$deleteQuery);

    foreach($quizzes as $quiz){
        $filename = $quiz['filename'];
        $filepath = realpath("../../quiz/generated/".$filename);

        if (file_exists($filepath)) {
            unlink($filepath);
            echo "success";
        } else {
            echo getcwd();
        }
    }


