```mermaid
classDiagram
    namespace Enums{
        class TransactionCategory{
            <<Enumeration>>
            +COMIDA
            +TRANSPORTE
            +HOGAR
            +SALUD
            +OCIO
            +SERVICIOS
            +EDUCACION
            +INGRESO_LABORAL
            +AHORRO
            +DEUDAS
            +OTROS
        }
        class TransactionType{
            <<Enumeration>>
            +INCOME
            +EXPENSE
        }
        class PaymentMethod{
            <<Enumeration>>
            +CREDIT
            +DEBIT
            +CASH
            +TRANSFER
        }
        class ActivityLevel{
            <<Enumeration>>
            +SEDENTARY
            +LIGHTLY_ACTIVE
            +MODERATELY_ACTIVE
            +VERY_ACTIVE
            +EXTREMELY_ACTIVE
            +multiplier() float
        }
        class GoalStrategy{
            <<Enumeration>>
            +AGGRESSIVE_CUT
            +MODERATE_CUT
            +MAINTENANCE
            +MUSCLE_GAIN
            +protein_factor() float
            +calorie_offset() int
        }
    }
    namespace Repositories{

    }
    namespace Schemas{

    }
    namespace Services{

    }
    namespace Routers{

    }
```