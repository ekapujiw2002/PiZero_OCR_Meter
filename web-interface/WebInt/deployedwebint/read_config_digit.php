<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

$numDigits = 7;
$fileName = 'outputs/digits_config_';
//$file = fopen($fileName,"w") or die("Error writing configuration file");
var_dump($_POST);
$configParams = "";


for( $i=0 ;$i < $numDigits; $i+=1){
	$file = fopen($fileName. $i .".txt","w");
	$currentDigit = "";
	for( $j=1; $j<=4; $j+=1){
		$pid  = "d".$i. "p" . $j;
		$currentDigit= $currentDigit. $_POST[$pid . "x"] . " " . $_POST[$pid. "y"] . "\n";
		
	}
	$currentDigit = $currentDigit. "\n";
	$configParams = $configParams . $currentDigit;
	fwrite($file,$currentDigit);
}

echo "Following parameters received:\n";
var_dump($configParams); echo "<br> To be saved in file <br>";
var_dump($file);	 echo "<br>";
// Write the contents back to the file
fwrite($file, $configParams);
fclose($file);

echo "Setting saved to file config.txt";

//Transform the image based on parameters
echo "<br> Running python script for processing <br>";
for($i=0; $i < $numDigits; $i+=1){
	echo "Currently on digit ".$i. "<br>";
	system("/home/pi/.virtualenvs/cv/bin/python3 transform.py ". $fileName . $i . ".txt outputs/warped.jpg " . "digits/digitWarped_". $i . ".jpg");
	echo "<br><br>";
}

echo "<br>Digits separated, for current reading access <a href=\"currentReading.html\"> currentReading.html </a> <br>";

?>
<h4>Navigation</h4>
<a href="index.html">Latest Image</a> | <a href="old-index.html">Region of Interest Selection </a> | <a href="digitSelect.html">Digit Selection</a> | <a href="currentReading.html">Currently read digits </a> | <a href="wifiControl.html">Change wifi configuration</a>

</body>
</html>
