<?php

$code = 'echo "ok";';
$req = curl_init("http://nginx-internal/process.php");
curl_setopt($req, CURLOPT_HTTPHEADER, array('Host: processor'));
curl_setopt($req, CURLOPT_POSTFIELDS, "code={$code}");
curl_setopt($req, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($req);
curl_close($req);

$status = [
    "frontend" => "ok",
    "processor" => $result,
];

echo json_encode($status);

?>
