<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $userID = $_POST["id"];

    if($userID){

        $totalCoursesQuery = "
        SELECT count(*) as courses
        FROM courses
        WHERE creatorID = '$userID'
        ";

        $totalStudentsQuery = "
        SELECT COUNT(*) as students
        FROM courses
        INNER JOIN subscriptions ON subscriptions.courseID = courses.id
        WHERE courses.creatorID = '$userID'
        ";

        $totalExamsQuery = "
        SELECT COUNT(*) as exams
        FROM courses
        INNER JOIN exam ON exam.courseID = courses.id
        WHERE creatorID = '$userID'
        ";

        $totalCoursesResult = mysqli_query($conn,$totalCoursesQuery);
        $totalCourses = mysqli_fetch_all($totalCoursesResult, MYSQLI_ASSOC);

        $totalStudentsResult = mysqli_query($conn,$totalStudentsQuery);
        $totalStudents = mysqli_fetch_all($totalStudentsResult, MYSQLI_ASSOC);

        $totalExamsResult = mysqli_query($conn,$totalExamsQuery);
        $totalExams = mysqli_fetch_all($totalExamsResult, MYSQLI_ASSOC);

        $counts = array_merge(
            $totalCourses[0],
            $totalStudents[0],
            $totalExams[0],
        );

        echo json_encode($counts);

    }
    else{
        echo json_encode(array("status" => "error"));
    }