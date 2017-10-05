<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

//$file = fopen($fileName,"w") or die("Error writing configuration file");

$configParams = $_POST;
echo "Following parameters received:\n";
var_dump($configParams); 

$pass = $_POST['password'];
$user = $_POST['user'];

echo "<br>";
if( strlen($pass) < 8){ 
	echo "Password must be at least 8 characters long. (Otherwise wpa_supplicant stops working)"; 
	echo "<br> <a href=\"index.html\">Input new Wifi configuration</a>";
	}
else{
	system("/usr/bin/sudo ./add_wifi_details.sh ". "\"".$user."\" \"".$pass. "\"");
	echo "Added the wi-fi details";
	}

?>


<br><br><br>
<form action="./update_pi_network_mode.php" method="post">
<input type="hidden" name="toMode" value="client">
<input type="submit" value="Restart to connect to configured Wi-fi"><br>
</form>
</body>
</html>
