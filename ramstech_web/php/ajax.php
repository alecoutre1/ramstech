<?php

$URL="http://localhost:4444/predict";

function send_error($code, $msg){
    http_response_code(500);
    header('Content-type: text/json');
    print('{ "error : "'.$code.', "error_msg" : "'.$msg.'" }');
}


$ch = curl_init($URL);

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

curl_setopt($ch, CURLOPT_POST, true);

$data = $_POST;


$file_name =  $_FILES['file']['tmp_name'];

$finfo = finfo_open(FILEINFO_MIME_TYPE);
$finfo = finfo_file($finfo, $fileName);


$RealTitleID = $_FILES['file']['name'];

$cFile = new CURLFile($file_name, 'audio/mp3', $RealTitleID);

$data['file'] = $cFile;


curl_setopt($ch, CURLOPT_POSTFIELDS, $data);


$result = curl_exec($ch);
$error = curl_error($ch);

if (curl_errno($ch)) {
    send_error(500, "Server is not responding");
}
else{
    $info = curl_getinfo($ch);
    # if($info['content_type'] != 'text/json'){
    #     echo "Error, unexpected content type\n";
    # }
    # else{
        http_response_code($info['http_code']);
        header('Content-type: text/json; charset=utf-8');
        print($result); 
#    }
}

curl_close($ch);



?>
