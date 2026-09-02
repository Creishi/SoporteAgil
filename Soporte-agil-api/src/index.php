<?php
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS");

$method = $_SERVER['REQUEST_METHOD'];

// Conexión a la base de datos (simulando la inyección de dependencias)
$host = getenv('DB_HOST') ?: 'db';
$dbname = getenv('DB_NAME') ?: 'soporte_agil';
$user = getenv('DB_USER') ?: 'admin';
$pass = getenv('DB_PASS') ?: 'admin_password';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["error" => "Error de conexión a la BD: " . $e->getMessage()]);
    exit;
}

// Enrutador básico de la API REST
if ($method === 'GET') {
    // Caso de uso: Ver Cola de Tickets Asignados / Ver Mis Tickets
    $stmt = $pdo->query("SELECT * FROM tickets ORDER BY fecha_creacion DESC");
    $tickets = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($tickets);

} elseif ($method === 'POST') {
    // Caso de uso: Crear Ticket
    $data = json_decode(file_get_contents("php://input"));
    
    if(!empty($data->titulo) && !empty($data->descripcion)) {
        $stmt = $pdo->prepare("INSERT INTO tickets (titulo, descripcion, estado) VALUES (?, ?, 'ABIERTO')");
        if($stmt->execute([$data->titulo, $data->descripcion])) {
            http_response_code(201); // 201 Created
            echo json_encode([
                "mensaje" => "Ticket creado exitosamente",
                "simulacion_observer" => "Correo de notificación encolado para el usuario."
            ]);
        }
    } else {
         http_response_code(400); // 400 Bad Request
         echo json_encode(["error" => "Faltan datos requeridos (titulo, descripcion)"]);
    }
} else {
    http_response_code(405); // 405 Method Not Allowed
    echo json_encode(["error" => "Método HTTP no soportado"]);
}
?>