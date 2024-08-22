<?php

    include "../databaseConnection.php"; 

    $conn = OpenConnection();

    $query = $_POST['query'];

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $queryResult = mysqli_query($conn,$query);
    $result = mysqli_fetch_all($queryResult,MYSQLI_ASSOC);

    echo json_encode($result);

