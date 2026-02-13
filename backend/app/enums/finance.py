from enum import Enum

class TransactionCategory(str, Enum):
    COMIDA = "Comida"
    TRANSPORTE = "Transporte"
    HOGAR = "Hogar"
    SALUD = "Salud"
    OCIO = "Ocio"
    SERVICIOS = "Servicios"
    EDUCACION = "Educación"
    INGRESO_LABORAL = "Ingreso Laboral"
    AHORRO = "Ahorro"
    DEUDAS = "Deudas"
    OTROS = "Otros"

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class PaymentMethod(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    CASH = "cash"
    TRANSFER = "transfer"

class FinancialHealthStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
