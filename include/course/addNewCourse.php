<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];
    $title = $_POST['title'];
    $courseCode = $_POST['courseCode'];
    $creatorID = $_POST['creatorID'];
    $image = $_POST['image'];
    $language = $_POST['language'];
    $isLanguage = $_POST['isLanguage'];
    

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        INSERT INTO courses (id, title, courseCode, creatorID, image, language, isLanguage)
        VALUES ('$id', '$title', '$courseCode', '$creatorID', '$image', '$language', '$isLanguage')
    ";

    $result = mysqli_query($conn,$query);

    if($result) echo "success";
