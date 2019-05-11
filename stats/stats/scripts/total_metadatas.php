<?php

require_once('config/db.php');

function getNumberMetadatas()
{
	global $db;
	$req = $db->prepare('SELECT count(id) as nb FROM stats');
	// Execute request
	$req->execute();
	$data = $req->fetch();
	$res = floor($data['nb']/2);
	return $res;
}

function getNumberMetadatasRebuild()
{
	global $db;
	$req = $db->prepare('SELECT count(id) as nb FROM stats_rebuild');
	// Execute request
	$req->execute();
	$data = $req->fetch();
	$res = $data['nb']
	return $res;
}

?>