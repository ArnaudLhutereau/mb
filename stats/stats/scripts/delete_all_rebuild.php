<?php

require_once('../config/db.php');
$req = $db->prepare('DELETE FROM stats_rebuild');
// Execute request
$req->execute();

// Redirect
header("Location: http://127.0.0.1/statistics.php");

?>
