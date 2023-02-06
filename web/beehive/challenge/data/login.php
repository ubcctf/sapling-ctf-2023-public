<?php

session_start();

if (empty($_SESSION['logfile'])) {
    $_SESSION['logfile'] = 'log/' . bin2hex(random_bytes(15)) . ".log";
    $handle = fopen($_SESSION['logfile'], "w");
    fclose($handle);
}

?>

<head>
    <title>BeeHive login</title>
</head>

<div style="display: flex; justify-content: center;">
    <form action="login.php" method="POST">
        <p style="text-align: center;">Login |  <?php echo "<a href='{$_SESSION['logfile']}'>View login log</a>"; ?> </p>
        <p>Username: <input type="text" name="username"/></p>
        <p>Password: <input type="password" name="password"/></p>
        <p style="text-align: center;"><input type="submit" value="Login"/></p>
    </form>
</div>

<?php

function log_login($data) {
    $logpath = $_SESSION['logfile'];
    $data .= file_get_contents($logpath);

    file_put_contents($logpath, $data);
}

$user = $_POST['username'] ?? null;
$pass = $_POST['password'] ?? null;

if (!empty($user) && !empty($pass)) {
    $adminuser = 'user';
    $adminpass = random_bytes(20);
    
    if ($user == $adminuser && $pass == $adminpass) {
        log_login("login success for {$user}\n");
        header('Location: index.php?include=dashboard.php');
    } else {
        log_login("login failed for {$user}\n");
        header('Location: index.php?include=login.php');
    }
}

?>
