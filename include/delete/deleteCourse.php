<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        SELECT image
        FROM `courses`
        WHERE id='$id'
    ";

    $imageQuery = mysqli_query($conn,$query);
    $images = mysqli_fetch_all($imageQuery,MYSQLI_ASSOC);

    $deleteQuery = "
    DELETE FROM `courses`
    WHERE id='$id'
    ";

    $deleteQueryResponse = mysqli_query($conn,$deleteQuery);

    foreach($images as $image){
        $filename = $image['image'];
        $filepath = realpath("../../uploads/".$filename);

        if (file_exists($filepath)) {
            unlink($filepath);
            echo "success";
        } else {
            echo getcwd();
        }
    }


