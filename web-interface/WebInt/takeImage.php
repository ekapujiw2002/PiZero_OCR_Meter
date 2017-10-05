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

echo "<br><br><a href=\"index.html\">Image Control </a> | <a href=\"old-index.html\">Region of Interest Selection </a> | <a href=\"digitSelect.html\">Digit Selection</a> | <a href=\"currentReading.html\">Currently read digits </a>  ";

//header("Location: http://raspberrypi.local/"); 	//Redirect user
die();

?>


</body>
</html>
