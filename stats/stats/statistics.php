<?php
include('scripts/total_metadatas.php');
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
				<h2>Statistics</h2>
				<p><b>Total of metadatas store on Block chain: </b><?php $nb = getNumberMetadatas(); echo $nb; ?> </p>
				<p><b>Total of metadatas rebuild with Block chain: </b><?php $nb = getNumberMetadatasRebuild(); echo $nb; ?> </p>
				<p><a href="scripts/delete_all.php">Delete all statistics of metadata storage</a></p>
				<p><a href="scripts/delete_all_rebuild.php">Delete all statistics of rebuild metadata</a></p>
			</div>
		</div>


		<?php
		include('footer.php');
		?>


	</div>


</body>
</html>