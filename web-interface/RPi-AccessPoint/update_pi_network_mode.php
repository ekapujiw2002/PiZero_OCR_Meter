<html>
<body>

<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

echo var_dump($_POST);
echo "System should restart";
if($_POST['toMode'] == "client"){
	system("/usr/bin/sudo ./restart_into_client.sh ");
}
else if ($_POST['toMode'] == "host"){
	system("/usr/bin/sudo ./restart_into_host.sh");
}
?>

<h4>Navigation</h4>
<a href="index.html">Latest Image</a> | <a href="old-index.html">Region of Interest Selection </a> | <a href="digitSelect.html">Digit Selection</a> | <a href="currentReading.html">Currently read digits </a> | <a href="wifiControl.html">Change wifi configuration</a>

</body>
</html>
