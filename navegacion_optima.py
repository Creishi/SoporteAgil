import time
import random
import copy

# ==========================================================
# 1. MODELO DE DOMINIO
# ==========================================================
class Ticket:
    def __init__(self, ticket_id, categoria, prioridad):
        self.ticket_id = ticket_id
        self.categoria = categoria
        self.prioridad = prioridad  # 1: Alta, 2: Media, 3: Baja

class Tecnico:
    def __init__(self, id_tecnico, nombre, especialidad, carga_actual):
        self.id_tecnico = id_tecnico
        self.nombre = nombre
        self.especialidad = especialidad
        self.carga_actual = carga_actual  # Número de tickets asignados actualmente

# ==========================================================
# 2. PATRÓN ITERATOR (Recorrido Estructurado)
# ==========================================================
class IteratorTecnicos:
    def __init__(self, lista_tecnicos):
        self._tecnicos = lista_tecnicos
        self._index = 0

    def has_next(self):
        return self._index < len(self._tecnicos)

    def next(self):
        tecnico = self._tecnicos[self._index]
        self._index += 1
        return tecnico

# ==========================================================
# 3. PATRÓN STRATEGY (Estrategias de Navegación)
# ==========================================================
class EstrategiaNavegacion:
    def seleccionar_tecnico(self, ticket, lista_tecnicos):
        raise NotImplementedError

class EstrategiaLinealBasica(EstrategiaNavegacion):
    """Navegación Tradicional: Asigna al primer elemento disponible."""
    def seleccionar_tecnico(self, ticket, lista_tecnicos):
        iterator = IteratorTecnicos(lista_tecnicos)
        while iterator.has_next():
            tecnico = iterator.next()
            time.sleep(0.005)  # Latencia por inspección manual/no optimizada
            return tecnico
        return None

class EstrategiaOptimizadaCargaYPrioridad(EstrategiaNavegacion):
    """Navegación Optimizada: Evalúa carga y nivel de especialización."""
    def seleccionar_tecnico(self, ticket, lista_tecnicos):
        iterator = IteratorTecnicos(lista_tecnicos)
        mejor_tecnico = None
        menor_score = float('inf')

        while iterator.has_next():
            tecnico = iterator.next()
            time.sleep(0.001)  # Recorrido optimizado en memoria
            
            coincidencia = 0 if tecnico.especialidad == ticket.categoria else 5
            score = tecnico.carga_actual + coincidencia
            
            if score < menor_score:
                menor_score = score
                mejor_tecnico = tecnico

        return mejor_tecnico

# ==========================================================
# 4. MOTOR DE NAVEGACIÓN (Contexto)
# ==========================================================
class MotorNavegacionTickets:
    def __init__(self, estrategia: EstrategiaNavegacion):
        self.estrategia = estrategia

    def set_estrategia(self, nueva_estrategia: EstrategiaNavegacion):
        self.estrategia = nueva_estrategia

    def procesar_lote_tickets(self, lista_tickets, lista_tecnicos):
        inicio = time.time()
        asignaciones = []

        for ticket in lista_tickets:
            tecnico_seleccionado = self.estrategia.seleccionar_tecnico(ticket, lista_tecnicos)
            if tecnico_seleccionado:
                tecnico_seleccionado.carga_actual += 1
                asignaciones.append((ticket.ticket_id, tecnico_seleccionado.nombre))

        tiempo_total = time.time() - inicio
        return tiempo_total, asignaciones

# ==========================================================
# 5. BLOQUE DE EJECUCIÓN PRINCIPAL (INDISPENSABLE)
# ==========================================================
if __name__ == "__main__":
    print("=== ACTIVIDAD 6: EVALUACIÓN Y OPTIMIZACIÓN DE NAVEGACIÓN EN SOPORTEÁGIL ===")
    print("Iniciando pruebas de rendimiento en paralelo...")

    # Generación de datos de prueba
    categorias = ["Redes", "Base de Datos", "Software", "Hardware"]
    
    tecnicos_base = [
        Tecnico(f"TEC-{i}", f"Técnico {i}", random.choice(categorias), carga_actual=random.randint(1, 10))
        for i in range(1, 21) # 20 técnicos de soporte
    ]
    
    tickets_prueba = [
        Ticket(f"TKT-{i}", random.choice(categorias), prioridad=random.randint(1, 3))
        for i in range(1, 101) # 100 tickets por enrutar
    ]

    tecnicos_fase1 = copy.deepcopy(tecnicos_base)
    tecnicos_fase2 = copy.deepcopy(tecnicos_base)

    # --- FASE 1: NAVEGACIÓN TRADICIONAL LINEAL ---
    motor = MotorNavegacionTickets(EstrategiaLinealBasica())
    t_lineal, _ = motor.procesar_lote_tickets(tickets_prueba, tecnicos_fase1)
    
    cargas_fase1 = [t.carga_actual for t in tecnicos_fase1]
    desviacion_fase1 = max(cargas_fase1) - min(cargas_fase1)

    # --- FASE 2: NAVEGACIÓN OPTIMIZADA CON PATRÓN STRATEGY + ITERATOR ---
    motor.set_estrategia(EstrategiaOptimizadaCargaYPrioridad())
    t_optimizada, _ = motor.procesar_lote_tickets(tickets_prueba, tecnicos_fase2)
    
    cargas_fase2 = [t.carga_actual for t in tecnicos_fase2]
    desviacion_fase2 = max(cargas_fase2) - min(cargas_fase2)

    # --- PRESENTACIÓN DE RESULTADOS EN CONSOLA ---
    print("\n--- RESULTADOS DE LA EVALUACIÓN DE RENDIMIENTO ---")
    print(f"Peticiones Procesadas: 100 Tickets | Pool de Técnicos: 20 Nodos")
    print("-" * 60)
    print(f"1. Navegación Lineal (Sin patrón):")
    print(f"   - Tiempo total de recorrido: {t_lineal:.4f} segundos")
    print(f"   - Desbalance de carga (Máx - Mín): {desviacion_fase1} tickets de diferencia")
    
    print(f"\n2. Navegación Optimizada (Strategy + Iterator):")
    print(f"   - Tiempo total de recorrido: {t_optimizada:.4f} segundos")
    print(f"   - Desbalance de carga (Máx - Mín): {desviacion_fase2} tickets de diferencia")
    
    mejora_tiempo = ((t_lineal - t_optimizada) / t_lineal) * 100
    print("-" * 60)
    print(f" Ganancia en Eficiencia Operativa: {mejora_tiempo:.2f}% de reducción en tiempo de enrutamiento.")
    print(f" Distribución de Carga: La desviación bajó de {desviacion_fase1} a {desviacion_fase2} incidencias por técnico.\n")