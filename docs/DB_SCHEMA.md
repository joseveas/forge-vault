# Esquema de Base de Datos (NoSQL)

```mermaid
erDiagram
    %% RELACIONES
    USER ||--o{ TRANSACTION : "registra (historial)"
    USER ||--o{ BIOMETRICS : "mide (historial)"
    USER ||--o{ FOOD_ENTRY : "consume (historial)"
    
    %% ENTIDAD PRINCIPAL (Documento Firestore)
    USER {
        string uid PK "ID de Firebase Auth"
        string email
        string full_name
        int age
        
        %% CARPETA FINANZAS (Configuración Actual)
        object finance "{ monthly_income, fixed_expenses[], monthly_budget }"
        
        %% CARPETA SALUD (Estado Actual)
        object health "{ height_cm, current_weight, activity_level, tdee_goal, macro_split, current_body_fat, goal_strategy }"
    }

    %% COLECCIONES HISTÓRICAS (Logs)

    TRANSACTION {
        string id PK
        float amount "Número (ej: 2000)"
        string category "Texto (ej: Comida)"
        string description "Texto (ej: Compré pan)"
        date date "ISO 8601"
        string type "income/expense"
        string method "credit, debit, cash"
        boolean is_fixed "True=Fijo, False=Variable"
    }

    FOOD_ENTRY {
        string id PK
        string name
        float calories
        float protein
        float carbs
        float fat
        date timestamp
    }

    BIOMETRICS {
        string id PK
        float weight_kg
        float waist_cm
        float neck_cm
        float body_fat_pct "Calculado"
        date timestamp
    }
```