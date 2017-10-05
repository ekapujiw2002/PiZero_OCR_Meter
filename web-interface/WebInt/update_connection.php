<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

//$file = fopen($fileName,"w") or die("Error writing configuration file");

$configParams = $_POST;
echo "Following parameters received:\n";
var_dump($configParams); echo "<br> To be saved in file <br>";
//var_dump($file);	 echo "<br>";
// Write the contents back to the file


echo "<br><br><a href=\"index.html\">Image Control </a> | <a href=\"old-index.html\">Region of Interest Selection </a> | <a href=\"digitSelect.html\">Digit Selection</a> | <a href=\"currentReading.html\">Currently read digits </a>  ";
?>


</body>
</html>
