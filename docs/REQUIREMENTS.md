# Requerimientos del proyecto

## 1.- Visión General
Aplicación personal para la gestión integral de **Finanzas** (gastos/ingresos) y **Salud** (macros/dieta), utilizando IA para facilitar la entrada de datos.

## 2.- Módulo de Finanzas
### Requerimientos
    - [ ] **Ingreso Rápido de Datos:** El usuario ingresa texto natural (ej: "Compré pan por 2000 pesos") y la IA extrae el monto, la categoría y la descripción.
    - [ ] **Categorización Automática:** La IA sugiere la categoría más probable basada en el texto.
    - [ ] **Reportes y Gráficos:** Visualización de gastos por categoría, tendencias mensuales, etc.
    - [ ] **Presupuestos:** Definición de límites de gasto por categoría y alertas cuando se acercan al límite.
    - [ ] **Alertas y Notificaciones:** Notificaciones push cuando se excede un presupuesto o se detecta un gasto inusual.
    - [ ] **Semáforo de Salud Mensual:** Una barra de progreso simple: `[Ingresos vs. Gastos]`. Si la barra de gastos supera el 80% de los ingresos antes del día 20, alerta roja.
    - [ ] **"Burn Rate" Diario (Gasto Permitido):** Un cálculo dinámico que me diga: *"Te quedan $200.000. Puedes gastar máximo $15.000 por día el resto del mes"*. Este es el KPI más útil para el día a día.
    - [ ] **Top 3 Fugas de Dinero:** Ranking automático de categorías (ej: #1 Comida a Domicilio, #2 Uber) para identificar dónde estoy fallando.
    - [ ] **Proyección de Ahorro:** Basado en mi ritmo actual, ¿con cuánto dinero terminaré el mes? (Positivo o Negativo).
### Datos Necesarios (Schema)
    - [ ] **Transaction:**
        - [ ] **amount:** Número (ej: 2000)
        - [ ] **category:** Texto (ej: "Comida")
        - [ ] **description:** Texto (ej: "Compré pan")
        - [ ] **date:** Fecha (ISO 8601)
        - [ ] **type:** Texto ("income" | "expense")
        - [ ] **method:** Texto ("credit", "debit", "cash")
        - [ ] **is_fixed:** Booleano (True = Gasto Fijo/Mensual, False = Gasto Variable)

## 3.- Módulo de Salud
### Requerimientos
    - [ ] **Registro de Comidas:** El usuario ingresa texto natural (ej: "Comí una hamburguesa de 500 calorías") y la IA extrae las calorías y la descripción.
    - [ ] **Cálculo Diario:** Ver mi progreso diario de Proteínas, Carbohidratos y Grasas vs. mi meta (Definición).
    - [ ] **Histórico de Peso:** Registrar mi peso y medidas (Cintura, Cuello) cada viernes.
    - [ ] **Ajuste de TDEE:** El sistema debe recalcular mis calorías base si cambio de peso drásticamente.
    - [ ] **Gráfico de Tendencia de Peso:** Visualización (Línea de tiempo) de la bajada de peso semanal vs. el objetivo proyectado.
    - [ ] **Mapa de Calor Calórico:** Ver rápidamente qué días del mes cumplí el déficit y cuáles me excedí (tipo GitHub contributions o calendario semáforo).
    - [ ] **KPIs (Indicadores Clave):** Tarjetas resumen en la pantalla principal:
        - "Total Kgs Bajados desde el Inicio".
        - "Promedio de Calorías esta semana".
        - "Días consecutivos cumpliendo macros (Racha)".
### Datos Necesarios (Schema)
    - [ ] **FoodEntry:**
        - [ ] **name:** Texto (ej: "Hamburguesa")
        - [ ] **calories:** Número (ej: 500)
        - [ ] **protein:** Número (ej: 25)
        - [ ] **carbs:** Número (ej: 40)  
        - [ ] **fat:** Número (ej: 15)
        - [ ] **date:** Fecha (ISO 8601)
    - [ ] **WeightEntry:**
        - [ ] **weight:** Número (ej: 70)
        - [ ] **waist:** Número (ej: 80)
        - [ ] **neck:** Número (ej: 40)
        - [ ] **date:** Fecha (ISO 8601)

## 4.- Requerimientos Técnicos
- **Frontend:** React + Vite (Hospedado en Vercel).
- **Backend:** Python FastAPI (Hospedado en Render).
- **Base de Datos:** Firebase Firestore (NoSQL).
- **IA:** Google Gemini 3 (Para procesar texto natural a JSON).
- **Autenticación:** Firebase Authentication (Google Sign-In).