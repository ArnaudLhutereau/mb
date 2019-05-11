<?php
require_once('config/db.php');

if(isset($_GET['first']) && isset($_GET['second']))
{
	// Calculate difference
	// First
	$req = $db->prepare('SELECT time_insertion FROM stats_rebuild WHERE key_name=:key_name');
	$req->execute(array(
	'key_name' => $_GET['first']));
	$first = $req->fetch();
	// Second
	$req = $db->prepare('SELECT time_insertion FROM stats_rebuild WHERE key_name=:key_name');
	$req->execute(array(
	'key_name' => $_GET['second']));
	$second = $req->fetch();

	$result = $second['time_insertion']-$first['time_insertion'];
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>MetaStats</title>
	<link rel="stylesheet" type="text/css" href="trucss.css">
</head>
<body>


	<div class="contain">

		<div class="header">
			<div class="bg-header"></div>
			<div class="border-header"></div>
			<div class="row">
				<div class="col-12 text-center">
					<img src="img/logo.png">
				</div>
			</div>
		</div>

		<?php
		include('navbar.php');
		?>
		
		<div class="row">
			<div class="col-12 bloc">
			    <?php
			    $adresse = $_SERVER['PHP_SELF'];
			    $i = 0;
			    $type="All";
			    $number=10;
			    foreach($_GET as $cle => $valeur){
			        if($cle == "number")
			        {
			        	$number = $valeur;
			        }
			        if($cle == "type")
			        {
			        	$type = $valeur;
			        }
			    }
			    ?>
				<p>Select the number you want to display last rebuild.</p>
				<div class="text-center">
					<div class="col-3">
						<a href="last_rebuild.php?number=10&type=<?php echo $type; ?>" class="button">10 entries</a>
					</div>
					<div class="col-3">
						<a href="last_rebuild.php?number=20&type=<?php echo $type; ?>" class="button">20 entries</a>
					</div>
					<div class="col-3">
						<a href="last_rebuild.php?number=50&type=<?php echo $type; ?>" class="button">50 entries</a>
					</div>
					<div class="col-3">
						<a href="last_rebuild.php?number=100&type=<?php echo $type; ?>" class="button">100 entries</a> 
					</div>
					
					
					
					
				</div>
				<br>
				<form action="last_rebuild.php" method="GET">
				<label>You can calculate time between two files:</label>
				<input type="text" name="first" placeholder="Key_name of the first">
				<input type="text" name="second" placeholder="Key_name of the second">
				<input type="submit" name="send" value="Calculate">
				<br>
				</form>
				<?php if(isset($_GET['first']) && isset($_GET['second']) ) {
					echo "<p><b>Result: </b>".$result." seconds</p><br>";
				}
				?>
				<br>
				<p>Time taken after all transaction of metadata of a file (means 4 transactions to blockchain + 8 requests to Redis)</p>
				<br>
				<table class="table">
							<tr>
								<th>Key</th>
								<th>Time insertion</th>
								<th>Time between the current rebuild and the previous</th>
								<th>Type (<a href="last_rebuild.php?number=<?php echo $number; ?>&type=Start">Start</a> - <a href="last_rebuild.php?number=<?php echo $number; ?>&type=Finish">Finish</a>)</th>
							</tr>
							<?php include('scripts/last_rebuild.php'); ?>
				</table>
				<br>

				<p><b>Average time between two rebuild : </b>
					<?php 
					if(isset($_GET['type']))
					{
						if($_GET['type'] != "All")
						{
							if(isset($_GET['number']))
							{
								$total_seconds=$total_seconds/$max;
							}
							else
							{
								$total_seconds=$total_seconds/$max;
							}
							echo $total_seconds; 
						}
					}
					else
					{
						echo "Please select \"Start\" or \"Finish\" option to see average time.";
					}
					?>
				</p>
			</div>
		</div>


		<?php
		include('footer.php');
		?>


	</div>


</body>
</html>