<?php
	
	define('DB_NAME', 'metablock');
	
	define('DB_USER', 'metablockdb');

	define('DB_PASSWORD', 'metablockpassword'); 

	define('DB_HOST', 'localhost');

	define('DB_CHARSET', 'utf8');
	try {
		$db = new PDO('mysql:host=' . DB_HOST . ';dbname='. DB_NAME . ';charset=' . DB_CHARSET . '', DB_USER, DB_PASSWORD);
	}
	catch (PDOException $e)
	{
		echo $e->getMessage();
	}
	
?>