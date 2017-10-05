<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$fileName = 'outputs/config.txt';
$file = fopen($fileName,"w") or die("Error writing configuration file");

$configParams = $_POST["p1x"] . " " . $_POST["p1y"]  . "\n" . 
		$_POST["p2x"] . " " . $_POST["p2y"] . "\n" .
		$_POST["p3x"] . " " . $_POST["p3y"] . "\n" .
		$_POST["p4x"] . " " . $_POST["p4y"];
echo "Following parameters received:\n";
var_dump($configParams); echo "<br> To be saved in file <br>";
var_dump($file);	 echo "<br>";
// Write the contents back to the file
fwrite($file, $configParams);
fclose($file);

echo "Setting saved to file config.txt";

//Transform the image based on parameters
echo "<br> Running python script for processing <br>";
system("/home/pi/.virtualenvs/cv/bin/python3 transform.py ". $fileName);

echo "<br>Image should have been processed, please proceed to digitSelect.html<br>";
echo "<br><br><a href=\"index.html\">Image Control </a> | <a href=\"old-index.html\">Region of Interest Selection </a> | <a href=\"digitSelect.html\">Digit Selection</a> | <a href=\"currentReading.html\">Currently read digits </a>  ";
?>


</body>
</html>
