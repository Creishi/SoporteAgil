import threading
import time
import queue
import random

# Simulación de un Message Broker distribuido
broker_eventos = queue.Queue()

# Métricas globales para la evaluación
metricas = {
    "tickets_procesados": 0,
    "notificaciones_enviadas": 0,
    "tiempo_inicio": 0
}

# ---------------------------------------------------------
# COMPONENTE 1: Servicio de Tickets (Simula Nodos de API)
# ---------------------------------------------------------
def nodo_creacion_tickets(id_nodo, cantidad_peticiones):
    """Simula un hilo recibiendo peticiones HTTP de usuarios."""
    for i in range(cantidad_peticiones):
        ticket_id = f"TKT-{id_nodo}-{i}"
        # Simula el tiempo de escritura en la Base de Datos
        time.sleep(random.uniform(0.01, 0.03)) 
        
        # Publica el evento en el Broker (Patrón Observer/Mediator)
        broker_eventos.put({"tipo": "NUEVO_TICKET", "ticket_id": ticket_id})
        metricas["tickets_procesados"] += 1

# ---------------------------------------------------------
# COMPONENTE 2: Servicio de Notificaciones (Simula Workers)
# ---------------------------------------------------------
def nodo_notificador_worker(id_worker):
    """Simula un hilo en un servidor remoto consumiendo la cola."""
    while True:
        try:
            # Consume el evento del broker. Timeout simula el fin de los datos.
            evento = broker_eventos.get(timeout=2) 
            
            # Simula latencia de red al enviar un correo SMTP (Operación lenta)
            time.sleep(random.uniform(0.05, 0.1)) 
            
            metricas["notificaciones_enviadas"] += 1
            broker_eventos.task_done() # Confirma procesamiento (ACK)
            
        except queue.Empty:
            break # Si no hay mensajes en 2 segundos, el worker se apaga

# ---------------------------------------------------------
# ORQUESTACIÓN Y SIMULACIÓN
# ---------------------------------------------------------
def iniciar_simulacion(num_nodos_api, num_workers, tickets_por_nodo):
    print(f"--- Iniciando Simulación ---")
    print(f"Nodos API: {num_nodos_api} | Nodos Worker: {num_workers} | Carga: {num_nodos_api * tickets_por_nodo} tickets")
    
    metricas["tiempo_inicio"] = time.time()
    
    hilos_api = []
    hilos_workers = []

    # 1. Levantar Nodos Notificadores (Consumers esperando mensajes)
    for i in range(num_workers):
        hilo = threading.Thread(target=nodo_notificador_worker, args=(f"Worker-{i}",))
        hilo.start()
        hilos_workers.append(hilo)

    # 2. Levantar Nodos de Tickets (Producers recibiendo tráfico)
    for i in range(num_nodos_api):
        hilo = threading.Thread(target=nodo_creacion_tickets, args=(f"API-{i}", tickets_por_nodo))
        hilo.start()
        hilos_api.append(hilo)

    # Esperar a que terminen de entrar los tickets
    for hilo in hilos_api:
        hilo.join()

    # Esperar a que el Broker quede vacío (Workers terminen)
    for hilo in hilos_workers:
        hilo.join()

    tiempo_total = time.time() - metricas["tiempo_inicio"]
    print(f"Tiempo total: {tiempo_total:.2f} segundos")
    print(f"Tickets procesados: {metricas['tickets_procesados']}")
    print(f"Notificaciones enviadas: {metricas['notificaciones_enviadas']}\n")
    return tiempo_total

if __name__ == "__main__":
    # Prueba Inicial: Sistema desbalanceado (1 Worker)
    print(">> FASE 1: Prueba de estrés inicial")
    iniciar_simulacion(num_nodos_api=5, num_workers=1, tickets_por_nodo=20)

# Reiniciar métricas
    metricas = {"tickets_procesados": 0, "notificaciones_enviadas": 0, "tiempo_inicio": 0}
    
    # Prueba Optimizada: Escalado horizontal (10 Workers)
    print(">> FASE 2: Sistema optimizado tras ajustes de arquitectura")
    iniciar_simulacion(num_nodos_api=5, num_workers=10, tickets_por_nodo=20)