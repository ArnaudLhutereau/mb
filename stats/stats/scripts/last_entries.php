<?php


// Decide the number
if(!isset($_GET['number']))
{
	$number = 10;
}
else
{
	$number = intval($_GET['number']);
}
if(!isset($_GET['type']))
{
	$type = "All";
}

if($type == "All")
{
	switch($number) {
	case 10:
		$req = $db->prepare('SELECT * FROM stats ORDER BY id desc LIMIT 10');
		break;
	case 20:
		$req = $db->prepare('SELECT * FROM stats ORDER BY id desc LIMIT 20');
		break;
	case 50:
		$req = $db->prepare('SELECT * FROM stats ORDER BY id desc LIMIT 50');
		break;
	case 100:
		$req = $db->prepare('SELECT * FROM stats ORDER BY id desc LIMIT 100');
		break;
	case 1000:
		$req = $db->prepare('SELECT * FROM stats ORDER BY id desc LIMIT 1000');
		break;
	default:
		$req = $db->prepare('SELECT * FROM stats ORDER BY id desc LIMIT 10');
		break;
	}	
}
elseif($type == "Start")
{
	switch($number) {
	case 10:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Start" ORDER BY id desc LIMIT 10');
		break;
	case 20:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Start" ORDER BY id desc LIMIT 20');
		break;
	case 50:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Start" ORDER BY id desc LIMIT 50');
		break;
	case 100:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Start" ORDER BY id desc LIMIT 100');
		break;
	case 1000:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Start" ORDER BY id desc LIMIT 1000');
		break;
	default:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Start" ORDER BY id desc LIMIT 10');
		break;
	}
}
else
{
	switch($number) {
	case 10:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Finish" ORDER BY id desc LIMIT 10');
		break;
	case 20:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Finish" ORDER BY id desc LIMIT 20');
		break;
	case 50:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Finish" ORDER BY id desc LIMIT 50');
		break;
	case 100:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Finish" ORDER BY id desc LIMIT 100');
		break;
	case 1000:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Finish" ORDER BY id desc LIMIT 1000');
		break;
	default:
		$req = $db->prepare('SELECT * FROM stats WHERE type="Finish" ORDER BY id desc LIMIT 10');
		break;
	}
}
// Prepare the request

// Execute request
$req->execute();
$i=0;
while($data = $req->fetch())
{
	$file[$i]=$data;
	$i=$i+1;
}
$i=$i-1;
$max = $i;
$i=0;
$total_seconds=0;
while($i<=$max)
{
	if($i==$max)
	{
		echo '
		<tr>
			<td>'.htmlentities($file[$i]['key_name'],ENT_QUOTES).'</td>
			<td>'.htmlentities($file[$i]['time_insertion'],ENT_QUOTES).'</td>
			<td>/</td>
			<td>'.htmlentities($file[$i]['type'],ENT_QUOTES).'</td>
		</tr>
		';
		$i=$i+1;
	}
	else
	{
		$diff =$file[$i]['time_insertion'] - $file[$i+1]['time_insertion'];
		if($type != "All")
		{
			$total_seconds = $total_seconds + $diff;
		}
		echo '
		<tr>
			<td>'.htmlentities($file[$i]['key_name'],ENT_QUOTES).'</td>
			<td>'.htmlentities($file[$i]['time_insertion'],ENT_QUOTES).'</td>
			<td>'.$diff.'</td>
			<td>'.htmlentities($file[$i]['type'],ENT_QUOTES).'</td>
		</tr>
		';
		$i=$i+1;
	}
	
}

?>