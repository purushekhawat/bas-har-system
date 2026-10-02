<?php
/**
 * Hostinger Cron Job Keep-Alive Bridge Script
 * Bharatiya Antariksh Station (BAS) Subsystem
 */

// Replace with your actual Live Backend URL (e.g., https://your-backend.onrender.com/api/ping)
$backend_url = isset($_GET['url']) ? $_GET['url'] : 'https://your-backend.onrender.com/api/ping';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $backend_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_USERAGENT, 'Hostinger-Cron-KeepAlive/1.0');

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);
curl_close($ch);

header('Content-Type: application/json');
echo json_encode([
    'timestamp' => date('Y-m-d H:i:s'),
    'status' => ($http_code === 200) ? 'SUCCESS' : 'FAILED',
    'http_code' => $http_code,
    'target_url' => $backend_url,
    'curl_error' => $error,
    'response' => json_decode($response)
]);
?>
