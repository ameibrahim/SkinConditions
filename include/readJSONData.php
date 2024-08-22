<?php

$filepath = $_POST['filepath'];

$fp = fopen($filepath, 'r');


if ($fp) {
    while (($line = fgets($fp)) !== false) {
        echo $line;
    }

    fclose($fp);
} else {
    echo "Failed to open the file.";
}
