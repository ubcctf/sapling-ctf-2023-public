<html>
    <head>
        <title>1337 intercom</title>
    </head>

    <div style="display: table; margin-right: auto; margin-left: auto;">
        <h1>1337 Hacker Ave. Intercom</h1>

        <p>Welcome to your apartment maintence portal!</p>
        <p>Use the pinger to check if individual is in the building and the pager to communicate with them.</p>
        <p>Remember, Tamara handles administration and Mark handles repairs.</p>

        <div style="width: 300px; float:left; height:100px; margin:10px">
            <form id="pinger" action="index.php" method="POST">
                <p style="text-align: center;">Pinger</p>
                <input type="hidden" name="func" value="ping"/>
                <div>
                    Person: <input type="text" name="subject" placeholder="Jamie"/>
                </div>
                <div>
                    <input type="submit" name="submit" value="Send"/>
                </div>
            </form>
        </div>

        <div style="width: 300px; float:left; height:200px; margin:10px">
            <form id="pager" action="index.php" method="POST">
                <p style="text-align: center;">Pager</p>
                <input type="hidden" name="func" value="page"/>
                <div>
                    Person: 
                    <input type="text" name="subject" placeholder="Ming"/>
                </div>
                <div>
                    Message
                    <textarea name="message"></textarea>
                </div>
                <div>
                    <input type="submit" name="submit" value="Send"/>
                </div>
            </form>
        </div>
        
        <div style="float:left; clear: left; outline: 1px solid black; ">
        <?php

        $func = $_POST['func'] ?? "";
        $subject = $_POST['subject'] ?? "";
        $message = $_POST['message'] ?? "";

        if (empty($func) || empty($subject)) {
            return;
        }

        function invalid($str) {
            if (str_contains($str, '\'') == 1 || str_contains($str, '\\') == 1 || str_contains($str, '%') == 1 || str_contains($str, '#') == 1) {
                return true;
            }

            return false;
        }

        if (invalid($subject) || invalid($message)) {
            echo 'invalid characters in subject or message';
            return;
        }

        if ($func == "ping") {
            $code = "ping('$subject');";
        } else if ($func == "page") {
            $code = "page('$subject', '$message');";
        } else {
            echo "invalid function";
            return;
        }

        $req = curl_init("http://nginx-internal/process.php");
        curl_setopt($req, CURLOPT_HTTPHEADER, array('Host: processor'));
        curl_setopt($req, CURLOPT_POSTFIELDS, "code={$code}");
        $result = curl_exec($req);
        curl_close($req);

        ?>
        </div>

    </div>
</html>
