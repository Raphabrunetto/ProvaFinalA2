<?php

$request_uri = $_SERVER['REQUEST_URI'];
$parsed_url = parse_url($request_uri);
parse_str($parsed_url['query'] ?? '', $query_params);

if (strpos($parsed_url['path'], '/payment') === 0) {
    $product_id = $query_params['product_id'] ?? null;

    $order_url = 'http://orders:3002/order';
    if ($product_id) {
        $order_url .= '?product_id=' . urlencode($product_id);
    }

    $orderJson = file_get_contents($order_url);
    $orderData = json_decode($orderJson, true);

    if (isset($orderData['error'])) {
        http_response_code(404);
        echo json_encode(['error' => $orderData['error']]);
        exit;
    }

    $response = [
        'status' => 'paid',
        'order' => $orderData
    ];

    header('Content-Type: application/json');
    echo json_encode($response);
} else {
    http_response_code(404);
    echo json_encode(['error' => 'Not found']);
}
