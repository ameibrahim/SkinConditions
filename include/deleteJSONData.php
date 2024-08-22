<?php
$filepath = $_POST['filepath'];

if (unlink($filepath)) {
    echo "success";
}
