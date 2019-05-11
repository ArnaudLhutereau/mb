<?php

require_once('../config/db.php');


// Receive information of the file
$request = $_GET['request'];

// Split request in two part :
// "FILE_NAME /// TIME_INSERTION"
$data = explode('///', $request);
// data[0] contains the key_name of the metadata
// data[1] contains the float of time_insertion in Redis

$req = $db->prepare('INSERT into stats (key_name, time_insertion, type) VALUES (:key_name, :time_insertion, :type)');
$req->execute(array(
	'key_name' => $data[0],
	'time_insertion' => $data[1],
	'type' => $data[2]));
print_r($db->errorInfo());
echo "Requete OK";


?>