<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $userID = $_POST["id"];

    if($userID){

        $totalCoursesQuery = "
        SELECT COUNT(*) as courses
        FROM `subscriptions`
        INNER JOIN courses ON courses.id = subscriptions.courseID
        WHERE subscriptions.userID = '$userID' AND status = 'true'
        ";

        $totalExamsQuery = "
        SELECT COUNT(*) as exams
        FROM exam
        INNER JOIN subscriptions ON subscriptions.courseID = exam.courseID
        WHERE subscriptions.userID = '$userID'
        ";

        $totalCoursesResult = mysqli_query($conn,$totalCoursesQuery);
        $totalCourses = mysqli_fetch_all($totalCoursesResult, MYSQLI_ASSOC);

        $totalExamsResult = mysqli_query($conn,$totalExamsQuery);
        $totalExams = mysqli_fetch_all($totalExamsResult, MYSQLI_ASSOC);

        $counts = array_merge(
            $totalCourses[0],
            $totalExams[0],
        );

        echo json_encode($counts);

    }
    else{
        echo json_encode(array("status" => "error"));
    }