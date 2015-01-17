<?php
$tmp_file_name = $_FILES['Filedata']['tmp_name'];
$sname = 'config.txt';
$pname = '/home/oeplse/html/'.$name;
$ok = move_uploaded_file($tmp_file_name, '/home/oeplse/data/'.$sname);

echo $name;
