<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $id = $_POST['id'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $query = "
        SELECT value
        FROM `resources`
        WHERE id='$id' AND type REGEXP '^image/' OR type REGEXP '^application/' OR type REGEXP '^video/'
    ";

    $resourcesQuery = mysqli_query($conn,$query);
    $resources = mysqli_fetch_all($resourcesQuery,MYSQLI_ASSOC);

    $deleteQuery = "
        DELETE FROM 
        `resources`
        WHERE subtopicID='$id' AND ( type REGEXP '^image/' OR type REGEXP '^application/' OR type REGEXP '^video/' )
    ";

    mysqli_query($conn,$deleteQuery);

    $deleteQuery = "
        DELETE FROM
        `subtopics`
        WHERE id='$id'
    ";

    mysqli_query($conn,$deleteQuery);

    foreach($resources as $resource){
        $filename = $resource['value'];
        $filepath = realpath("../../uploads/".$filename);

        if (file_exists($filepath)) {
            unlink($filepath);
        } else {
            echo getcwd();
        }
    }

    echo "success";


