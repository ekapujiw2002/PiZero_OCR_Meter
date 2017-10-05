<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<br> Running image capture script <br>";

//Make really sure that the new image gets put there
system("yes | cp /var/www/html/latestManual.jpg /var/www/html/exlatestManual.jpg");	//Save the last one
system("yes | rm /var/www/html/latestManual.jpg");					//Remove the last one so no overwrite conflicts occur
system("yes | /home/pi/webcam/capture.sh /var/www/html/latestManual.jpg");		//Make new  picture

//Redirect user
//header("Location: http://raspberrypi.local/"); 	//Redirect user
die();

?>
<h4>Navigation</h4>
<a href="index.html">Latest Image</a> | <a href="old-index.html">Region of Interest Selection </a> | <a href="digitSelect.html">Digit Selection</a> | <a href="currentReading.html">Currently read digits </a> | <a href="wifiControl.html">Change wifi configuration</a>

</body>
</html>
