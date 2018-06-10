<?php
$tmp_file_name = $_FILES['Filedata']['tmp_name'];
$sname = 'log_'.date('d-m-Y_H:i');
$name =$sname.'.bin';
$pname = '/home/oeplse/html/'.$name;
$ok = move_uploaded_file($tmp_file_name, '/home/oeplse/data/'.$name);

$pname = $sname.'.png';
system('python2.7 vis.py /home/oeplse/data/'.$name);

$ook = copy('/home/oeplse/data/'.$pname, '/home/oeplse/html/'.$pname);

$ppath='/home/oeplse/html/'.$pname;

echo $pname;
