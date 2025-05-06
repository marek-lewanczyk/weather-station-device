<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $config = [
        'device_name' => $_POST['device_name'],
        'wifi_ssid' => $_POST['ssid'],
        'wifi_password' => $_POST['password'],
        'sampling_interval' => (int)$_POST['sampling_interval'],
        'temperature_unit' => $_POST['temperature_unit'],
        'location_description' => $_POST['location_description'],
        'log_to_db' => isset($_POST['log_to_db']) ? true : false
    ];

    file_put_contents('config.json', json_encode($config, JSON_PRETTY_PRINT));
    echo "Konfiguracja zapisana pomyślnie!";
} else {
    echo "Nieprawidłowe żądanie.";
}
?>
