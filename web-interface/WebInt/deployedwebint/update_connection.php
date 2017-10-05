<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

//$file = fopen($fileName,"w") or die("Error writing configuration file");

$configParams = $_POST;
echo "Following parameters received:\n";
var_dump($configParams); echo "<br> To be saved in file <br>";

$pass = $_POST['password'];
$user = $_POST['user'];

system("/usr/bin/sudo ./add_wifi_details.sh ". "\"".$user."\" \"".$pass. "\"");
echo "Hopefully added the wi-fi details";
//var_dump($file);	 echo "<br>";
// Write the contents back to the file


?>
<h4>Navigation</h4>
<a href="index.html">Latest Image</a> | <a href="old-index.html">Region of Interest Selection </a> | <a href="digitSelect.html">Digit Selection</a> | <a href="currentReading.html">Currently read digits </a> | <a href="wifiControl.html">Change wifi configuration</a>

</body>
</html>
