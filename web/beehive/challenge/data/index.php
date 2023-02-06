<html>
    <?php
    ini_set('display_errors', 1);
    
    $file = $_GET['include'] ?? null;
    if (empty($file) || str_contains($file, "..") || str_starts_with($file, "/")) {
        $file = 'login.php';
    }

    include $file;

    ?>
</html>
