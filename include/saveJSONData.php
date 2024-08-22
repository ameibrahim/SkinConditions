<?php

$filepath = $_POST['filepath'];
$jsonString = $_POST['jsonString'];

$fp = fopen($filepath, 'w');
fwrite($fp, $jsonString);
fclose($fp);

echo "success";