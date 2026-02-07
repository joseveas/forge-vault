# Casos de Uso

## Actores
    * **Usuario (Yo):** Usuario principal de la aplicación.
    * **Sistema:** Sistema de gestión de finanzas y salud.
    * **IA (Gemini):** Asistente virtual para el procesamiento de texto natural.

## Modulo A: Finanzas
### **UC-A-01: Ingresar Gastos con IA**
**Nivel:** Crítico
**Descripción:** El Admin ingresa texto natural y el sistema estructura la data para su confirmación.
**Pre-condiciones:**
    * Admin autenticado.
**Flujo Principal:**
    1. El Admin escribe: "Compré pan por 2000".
    2. El Sistema envía el texto a Gemini (Backend).
    3. La IA procesa y devuelve un JSON estructurado.
    4. **El Sistema muestra una "Tarjeta Borrador" con los datos detectados (Monto: 2000, Cat: Comida).**
    5. El Admin revisa y hace clic en "Confirmar Guardado".
    6. El Sistema guarda en Firestore y actualiza el Dashboard.
**Flujo Alternativo:**
    * **A1 (Corrección Manual):** En el paso 4, si la IA clasificó mal (ej: puso "Ocio" en vez de "Comida"), el Admin edita el campo manualmente antes de confirmar.
    * **A2 (Texto incomprensible):** Si la IA no entiende nada, el Sistema devuelve: *"No pude entender el gasto. Por favor intenta ser más específico"*.
**Post-condiciones:**
    * El gasto se guarda en la base de datos.
    * El Admin ve una notificación de éxito.

### **UC-A-02: Consultar Salud Financiera (Dashboard)**
**Nivel:** Crítico
**Descripción:** El Admin revisa su estado financiero en tiempo real para tomar decisiones de gasto inmediato.
**Pre-condiciones:**
    * El Admin está logueado.
    * El presupuesto mensual está configurado.
**Flujo Principal:**
    1. El Admin abre la aplicación (Home).
    2. El Sistema obtiene el total de ingresos, gastos fijos y gastos variables del mes.
    3. **El Sistema calcula el "Burn Rate":** `(Presupuesto - Gastado) / Días Restantes`.
    4. El Sistema muestra una Tarjeta Principal con el **"Semáforo"**:
        * 🟢 **Verde:** "Puedes gastar $15.000 hoy".
        * 🔴 **Rojo:** "¡Alto! Te has excedido en $50.000".
    5. El Sistema muestra debajo la lista de "Últimos Movimientos".
**Flujos Alternativos:**
    * **A1 (Mes Nuevo / Sin Datos):** Si no hay transacciones en el mes actual, el Sistema muestra: *"Mes limpio. Tu saldo diario inicial es $X. ¡Empieza a registrar!"*.
    * **A2 (Presupuesto No Configurado):** Si no hay presupuesto definido, el Sistema muestra una alerta: *"Configura tu límite mensual para ver el semáforo"*.
**Post-condiciones:**
    * El Admin ve un dashboard con sus gastos e ingresos.

### **UC-A-03: Configurar Presupuesto Mensual**
**Nivel:** Alta
**Descripción:** El Admin define sus ingresos y gastos fijos para calcular el "Dinero Realmente Disponible" (Disposable Income).
**Pre-condiciones:**
    * El Admin está logueado.
**Flujo Principal:**
    1. El Admin accede a "Configuración de Presupuesto".
    2. El Admin ingresa su **Ingreso Líquido Mensual** (ej: $1.500.000).
    3. El Admin lista sus **Gastos Fijos Obligatorios** (Arriendo, Créditos, Internet, Luz).
    4. **El Sistema calcula el "Presupuesto Variable":** `Ingreso - Suma(Fijos)`.
        * *Ejemplo: 1.5M - 800k Fijos = $700.000 para gastar en el mes.*
    5. El Sistema guarda esta configuración como la "Meta del Mes".
    6. El Sistema recalcula inmediatamente el Semáforo del Dashboard.
**Flujos Alternativos:**
    * **A1 (Gastos > Ingresos):** Si los Fijos superan al Ingreso, el Sistema muestra alerta crítica: *"¡Tus costos fijos superan tu sueldo! Imposible calcular presupuesto positivo"*.
**Post-condiciones:**
    * El presupuesto se guarda en la base de datos.
    * El Admin ve una notificación de éxito.

### **UC-A-04: Editar Transacción**
**Nivel:** Media
**Descripción:** El Admin corrige errores en el monto, fecha o categoría de un registro histórico.
**Pre-condiciones:**
    * El Admin está logueado.
    * La transacción existe y no está bloqueada (ej: conciliada).
**Flujo Principal (Happy Path):**
    1. El Admin selecciona una transacción y presiona "Editar" (Lápiz).
    2. El Sistema despliega un formulario pre-llenado con los datos actuales.
    3. El Admin modifica el campo erróneo (ej: Cambia categoría de "Ocio" a "Comida").
    4. El Admin presiona "Guardar Cambios".
    5. **El Sistema valida la integridad (ej: que el monto no sea negativo).**
    6. El Sistema actualiza el documento en Firestore.
    7. **El Sistema dispara un re-cálculo del Dashboard y Presupuesto del mes afectado.**
    8. El Sistema muestra notificación: *"Transacción actualizada y saldos recalculados"*.
**Flujos Alternativos:**
    * **A1 (Cancelación sin cambios):** Si el Admin presiona "Cancelar" o cierra el modal, el Sistema descarta los cambios y mantiene el estado original.
    * **A2 (Error de Validación):** Si el Admin borra el monto o pone texto en un campo numérico, el Sistema bloquea el guardado y marca el campo en rojo.
**Post-condiciones:**
    * La transacción se guarda en la base de datos.
    * El Admin ve una notificación de éxito.

### **UC-A-05: Eliminar Transacción**
**Nivel:** Media
**Descripción:** El Admin elimina permanentemente un registro de gasto o ingreso erróneo.
**Pre-condiciones:**
    * El Admin está logueado.
    * Existe al menos una transacción en el historial.
**Flujo Principal (Happy Path):**
    1. El Admin identifica una transacción en la lista y presiona el ícono "Eliminar" (Papelera).
    2. El Sistema muestra un modal de advertencia: *"¿Estás seguro de borrar este gasto?"*.
    3. El Admin confirma la acción (Click en "Sí, borrar").
    4. El Sistema elimina el documento de Firestore.
    5. El Sistema recalcula el saldo total y refresca la lista del Dashboard.
    6. El Sistema muestra notificación flotante (Toast): *"Transacción eliminada correctamente"*.
**Flujos Alternativos:**
    * **A1 (Cancelación):** En el paso 2, si el Admin presiona "Cancelar" o cierra el modal, el sistema no realiza ninguna acción y mantiene la transacción.
    * **A2 (Fallo de Red):** En el paso 4, si la base de datos no responde (sin internet), el Sistema muestra: *"Error de conexión: No se pudo eliminar el registro. Intente nuevamente"*.
**Post-condiciones:**
    * La transacción se elimina de la base de datos.
    * El Admin ve una notificación de éxito.

## Módulo B: Salud & Macros

### **UC-B-01: Loggear Comida con IA**
**Nivel:** Crítico
**Descripción:** El Admin registra una comida usando lenguaje natural y el sistema estima calorías y macros.
**Pre-condiciones:**
    * El Admin está logueado.
    * Existen metas de macros configuradas (UC-B-04).
**Flujo Principal (Happy Path):**
    1. El Admin escribe: *"200g de pechuga de pollo a la plancha y una taza de arroz blanco"*.
    2. El Sistema envía el texto a **Gemini (Backend)**.
    3. La IA procesa y devuelve un JSON estimado:
       ```json
       {
         "name": "Pollo a la plancha con arroz",
         "calories": 450,
         "protein": 50,  // gramos
         "carbs": 45,    // gramos
         "fat": 5,       // gramos
         "date": "2023-10-27T14:30:00"
       }
       ```
    4. **El Sistema muestra la "Tarjeta Borrador"**.
    5. El Admin revisa y confirma (o ajusta si sabe que el arroz eran 300g).
    6. El Sistema guarda el registro en Firestore.
    7. El Sistema resta los valores de la "Meta Diaria" y actualiza el Dashboard.
**Flujos Alternativos:**
    * **A1 (Alimento desconocido):** Si la IA dice "No sé qué es 'Gagh'", el sistema pide aclarar el alimento.
    * **A2 (Edición Manual):** En el paso 5, el Admin corrige los gramos de proteína manualmente porque leyó la etiqueta del envase.
**Post-condiciones:**
    * La comida se guarda en la base de datos.
    * El Admin ve una notificación de éxito.

### **UC-B-02: Consultar Dashboard Nutricional**
**Nivel:** Alto
**Descripción:** Visualizar el progreso diario de ingesta (consumido) vs. objetivos (TDEE/Macros) en tiempo real.
**Pre-condiciones:**
    * El Admin está logueado.
    * **Las Metas de Macros (UC-B-04) están configuradas.**
**Flujo Principal (Happy Path):**
    1. El Admin entra a la pestaña de Salud/Dashboard.
    2. El Sistema obtiene todos los registros de comida (`FoodEntry`) con fecha de **hoy**.
    3. El Sistema recupera las Metas Diarias del perfil (ej: 1800 kcal).
    4. El Sistema suma los totales consumidos: (Calorías: 1200, Prot: 100, etc.).
    5. El Sistema calcula el restante: `Meta - Consumido`.
    6. El Sistema muestra 3 Barras de Progreso (Prot, Carb, Grasas) y el contador principal de Calorías Restantes.
    7. **Lógica Visual:** Si el consumo supera la meta en algún macro, esa barra específica cambia a color rojo (alerta).
**Flujos Alternativos:**
    * **A1 (Sin Metas Configuradas):** Si el sistema detecta que no hay metas guardadas, muestra un botón ("Call to Action"): *"Configura tu Plan Nutricional para empezar a medir"*.
    * **A2 (Día Vacío):** Si no hay registros de comida hoy, el Sistema muestra las barras en 0% y el mensaje: *"Día limpio. ¡Registra tu primera comida!"*.
    * **A3 (Error de Carga):** Si falla la conexión, muestra los últimos datos cacheados con un icono de "Sin conexión".
**Post-condiciones:**
    * La interfaz refleja el estado exacto de la ingesta diaria.
    * No se modifican datos en la base de datos (lectura).

### **UC-B-03: Check-in Biométrico (Viernes)**
**Nivel:** Crítico
**Descripción:** Registrar medidas corporales para calcular % Grasa y ajustar la dieta.
**Pre-condiciones:**
    * Es día de medición (o el usuario decide hacerlo).
**Flujo Principal:**
    1. El Admin ingresa: Peso (kg), Cintura (cm) y Cuello (cm).
    2. **El Sistema aplica la fórmula de Grasa Corporal (Marina EEUU):**
       * *Cálculo interno basado en altura (fija), cintura y cuello.*
    3. El Sistema guarda el registro histórico.
    4. El Sistema calcula la variación respecto a la semana anterior (ej: "-0.5% Grasa").
    5. El Sistema muestra feedback: *"¡Bajaste grasa y mantuviste peso! Vas bien."*.
**Flujo Alternativo:**
    * **A1 (Aumento de Peso):** Si el peso subió, el Sistema pregunta: *"¿Subiste de peso? Revisa tus calorías de la semana"*.
    * **A2 (Sin Cambio):** Si no hay cambios, el Sistema muestra: *"Peso estable. Sigue así"*.
    * **A3 (Cancelación):** Si el Admin presiona "Cancelar" o cierra el modal, el Sistema descarta los cambios y mantiene el estado original.
    * **A4 (Fallo de Red):** En el paso 3, si la base de datos no responde (sin internet), el Sistema muestra: *"Error de conexión: No se pudo guardar el registro. Intente nuevamente"*.
    * **A5 (Fallo de Validación):** En el paso 1, si el Admin ingresa texto en un campo numérico, el Sistema bloquea el guardado y marca el campo en rojo.
**Post-condiciones:**
    * El registro se guarda en la base de datos.
    * El Admin ve una notificación de éxito.

### **UC-B-04: Configurar Metas (TDEE)**
**Nivel:** Crítico
**Descripción:** Definir los parámetros base del cuerpo y el objetivo (Déficit/Superávit) para calcular los macros diarios.
**Pre-condiciones:**
    * El Admin está logueado.
**Flujo Principal (Happy Path):**
    1. El Admin ingresa sus datos base: Edad, Altura, Nivel de Actividad (Sedentario/Activo).
    2. El Sistema calcula el **TDEE (Gasto Energético Total)** usando la fórmula Mifflin-St Jeor.
    3. El Admin selecciona objetivo: "Perder Peso (Definición)" o "Ganar Músculo (Volumen)".
    4. El Sistema aplica el recorte/aumento (ej: -500 kcal) y establece las nuevas **Metas Diarias** de Macros.
    5. El Sistema guarda la configuración en Firestore.
    6. El Sistema muestra: *"Metas actualizadas: Tu nuevo límite es 1800 kcal"*.
**Flujos Alternativos:**
    * **A1 (Datos Irreales):** Si el Admin ingresa números imposibles (ej: Altura 3 metros, Edad 200 años), el Sistema muestra error: *"Datos biométricos fuera de rango. Revisa la entrada"*.
    * **A2 (Fallo de Guardado):** Si Firestore falla, el Sistema muestra: *"No se pudo actualizar la meta. Se mantendrá la configuración anterior"*.
**Post-condiciones:**
    * Las nuevas metas de Macros reemplazan a las anteriores inmediatamente.
    * El Dashboard del día en curso se recalcula con los nuevos límites (las barras de progreso cambian de tamaño).
