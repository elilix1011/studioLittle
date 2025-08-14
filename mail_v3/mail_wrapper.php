<?php
// CGIファイルをPHPでラップして実行
$cgi_file = __DIR__ . '/mail.cgi';

// 環境変数を設定
putenv("REQUEST_METHOD=" . $_SERVER['REQUEST_METHOD']);
putenv("QUERY_STRING=" . $_SERVER['QUERY_STRING']);
putenv("CONTENT_TYPE=" . $_SERVER['CONTENT_TYPE']);
putenv("CONTENT_LENGTH=" . $_SERVER['CONTENT_LENGTH']);
putenv("REQUEST_URI=" . $_SERVER['REQUEST_URI']);
putenv("DOCUMENT_ROOT=" . $_SERVER['DOCUMENT_ROOT']);
putenv("SERVER_PROTOCOL=" . $_SERVER['SERVER_PROTOCOL']);
putenv("GATEWAY_INTERFACE=CGI/1.1");
putenv("SERVER_SOFTWARE=nginx");
putenv("REMOTE_ADDR=" . $_SERVER['REMOTE_ADDR']);
putenv("REMOTE_PORT=" . $_SERVER['REMOTE_PORT']);
putenv("SERVER_ADDR=" . $_SERVER['SERVER_ADDR']);
putenv("SERVER_PORT=" . $_SERVER['SERVER_PORT']);
putenv("SERVER_NAME=" . $_SERVER['SERVER_NAME']);

// POSTデータを標準入力に渡す
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = file_get_contents('php://input');
    if (empty($input)) {
        $input = http_build_query($_POST);
    }
    $descriptorspec = array(
        0 => array("pipe", "r"),  // stdin
        1 => array("pipe", "w"),  // stdout
        2 => array("pipe", "w")   // stderr
    );
    
    $process = proc_open("perl $cgi_file", $descriptorspec, $pipes);
    
    if (is_resource($process)) {
        fwrite($pipes[0], $input);
        fclose($pipes[0]);
        
        $output = stream_get_contents($pipes[1]);
        $error = stream_get_contents($pipes[2]);
        
        fclose($pipes[1]);
        fclose($pipes[2]);
        
        $return_value = proc_close($process);
        
        if ($return_value === 0) {
            echo $output;
        } else {
            echo "Error: $error";
        }
    }
} else {
    // GETリクエストの場合
    $output = shell_exec("perl $cgi_file");
    echo $output;
}
?>
