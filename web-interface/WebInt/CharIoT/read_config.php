<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$file = fopen('outputs/config.txt',"w") or die("Error writing configuration file");

$configParams = $_POST["p1x"] . " " . $_POST["p1y"] . "\n" .
		$_POST["p2x"] . " " . $_POST["p2y"] . "\n" .
		$_POST["p3x"] . " " . $_POST["p3y"] . "\n" .
		$_POST["p4x"] . " " . $_POST["p4y"];
echo "Following parameters received:\n";
var_dump($configParams); echo "<br> To be saved in file <br>";
var_dump($file);	 echo "<br>";
// Write the contents back to the file
fwrite($file, $configParams);
fclose($file);
echo "Setting saved to file config.txt"
?>


</body>
</html>
