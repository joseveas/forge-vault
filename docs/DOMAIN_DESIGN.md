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
        class FinancialHealthStatus {
            <<Enumeration>>
            +HEALTHY
            +WARNING
            +CRITICAL
        }
    }
    namespace Repositories{
        class BaseModel {
            <<Pydantic>>
        }
        class FirestoreRepository~ModelType, CreateSchemaType, UpdateSchemaType~ {
            <<Abstract>>
            +collection_name: str
            +model: Type~ModelType~
            +db: Client
            +__init__(collection_name: str, model: Type~ModelType~)
            +get(doc_id: str) Optional~ModelType~
            +create(obj_in: CreateSchemaType, user_id: str, custom_id: str = None) ModelType
            +update(doc_id: str, obj_in: UpdateSchemaType) Optional~ModelType~
            +delete(doc_id: str) bool
        }
        class UserRepository {
            +__init__()
        }
        class FinanceRepository {
            +__init__()
            +get_by_date_range(user_id: str, start_date: date, end_date:date) List~TransactionResponse~
        }
        class NutritionRepository {
            +__init__()
            +get_by_date_range(user_id: str, start: date, end: date) List~DailyLogResponse~
        }
        class BiometricsRepository {
            +__init__()
            +get_latest(user_id: str) Optional~BiometricEntryResponse~
            +get_history(user_id: str, start: date, end: date) List~BiometricEntryResponse~
        }
    }
    UserRepository --|> FirestoreRepository : <UserResponse, UserCreate, UserUpdate>
    FinanceRepository --|> FirestoreRepository : <TransactionResponse, TransactionCreate, TransactionUpdate>
    NutritionRepository --|> FirestoreRepository : <DailyLogResponse, DailyLogCreate>
    BiometricsRepository --|> FirestoreRepository : <BiometricEntryResponse, BiometricEntryCreate>

    namespace Schemas{
        class BaseModel {
            <<Pydantic>>
        }
        class FixedExpenseTemplate {
            +name: str
            +amount: float
            +category: TransactionCategory
        }
        class MacroSplit {
            +protein_grams: float
            +carbs_grams: float
            +fat_grams: float
        }
        class FinanceConfig {
            +monthly_income: Optional~float~
            +fixed_expenses: List~FixedExpenseTemplate~
            +monthly_budget: Optional~float~
        }
        class HealthConfig {
            +height_cm: float
            +current_weight: Optional~float~
            +current_body_fat: Optional~float~
            +activity_level: ActivityLevel
            +goal_strategy: GoalStrategy
            +tdee_goal: Optional~float~
            +macro_split: Optional~MacroSplit~
        }
        class UserBase {
            <<Abstract>>
            +email: EmailStr
            +full_name: Optional~str~
            +age: int
            +finance: FinanceConfig
            +health: HealthConfig
        }
        class UserCreate {
            +firebase_uid: str
        }
        class UserUpdate {
            +full_name: Optional~str~
            +age: Optional~int~
            +finance: Optional~FinanceConfig~
            +health: Optional~HealthConfig~
        }
        class UserResponse {
            +id: str
            +user_id: str
            +created_at: datetime
        }
        class TransactionBase {
            <<Abstract>>
            +amount: float
            +category: TransactionCategory
            +description: str
            +date: date
            +type: TransactionType
            +method: PaymentMethod
            +is_fixed: bool
        }
        class TransactionCreate {
        }
        class TransactionUpdate {
            +amount: Optional~float~
            +category: Optional~TransactionCategory~
            +description: Optional~str~
            +is_fixed: Optional~bool~
        }
        class TransactionResponse {
            +id: str
            +user_id: str
            +created_at: Optional~datetime~
        }
        class CategorySpending {
            +category: TransactionCategory
            +amount: float
            +percentage: float
        }
        class MonthlyDashboardResponse {
            +current_month_total: float
            +budget_status: FinancialHealthStatus
            +burn_rate_daily: float
            +projected_savings: float
            +top_expenses: List~CategorySpending~
            +remaining_budget: float
        }
        class BiometricsBase {
            <<Abstract>>
            +weight_kg: float
            +waist_cm: float
            +neck_cm: float
            +notes: Optional~str~
        }
        class BiometricsUpdate {
            +weight_kg: Optional~float~
            +waist_cm: Optional~float~
            +neck_cm: Optional~float~
            +notes: Optional~str~
        }
        class BiometricsCreate {
            +date: date
        }
        class BiometricsResponse {
            +id: str
            +user_id: str
            +date: date
            +body_fat_pct: Optional~float~
            +lean_mass_kg: Optional~float~
            +fat_mass_kg: Optional~float~
        }
        class FoodItem {
            +name: str
            +quantity_label: str
            +calories: float
            +protein: float
            +carbs: float
            +fat: float
        }
        class DailyLogBase {
            <<Abstract>>
            +date: date
            +items: List~FoodItem~
            +total_calories: float
            +total_protein: float
            +total_carbs: float
            +total_fat: float
            +calories_goal: bool
        }
        class DailyLogUpdate {
            +items: List~FoodItem~
            +total_calories: float
            +total_protein: float
            +total_carbs: float
            +total_fat: float
            +calories_goal: bool
        }
        class DailyLogCreate {
        }
        class DailyLogResponse {
            +id: str
            +user_id: str
        }
        class MacroStatus {
            +protein_consumed: float
            +protein_goal: float
            +carbs_consumed: float
            +carbs_goal: float
            +fat_consumed: float
            +fat_goal: float
            +calories_remaining: float
        }
        class HealthDashboardResponse {
            +today_macros: MacroStatus
            +current_weight: float
            +total_weight_lost: float
            +weekly_avg_calories: float
            +days_in_deficit_streak: int
            +body_fat_pct: Optional~float~
        }
    }
    UserResponse --|> UserBase: inherit
    UserCreate --|> UserBase: inherit
    FixedExpenseTemplate --> TransactionCategory: use
    FinanceConfig *-- FixedExpenseTemplate: contain ~List~
    HealthConfig *-- MacroSplit: contain
    HealthConfig --> ActivityLevel: use
    HealthConfig --> GoalStrategy: use
    UserBase *-- FinanceConfig: contain
    UserBase *-- HealthConfig: contain
    UserUpdate *-- FinanceConfig: contain
    UserUpdate *-- HealthConfig: contain
    TransactionResponse --|> TransactionBase: inherit
    TransactionCreate --|> TransactionBase: inherit
    TransactionBase --> TransactionCategory: use
    TransactionBase --> TransactionType: use
    TransactionBase --> PaymentMethod: use
    TransactionUpdate --> TransactionCategory: use
    BiometricsResponse --|> BiometricsBase: inherit
    BiometricsCreate --|> BiometricsBase: inherit
    DailyLogBase *-- FoodItem: contain ~List~
    DailyLogCreate --|> DailyLogBase: inherit
    DailyLogResponse --|> DailyLogBase: inherit
    DailyLogUpdate *-- FoodItem: contain ~List~
    CategorySpending --> TransactionCategory: use
    MonthlyDashboardResponse --> FinancialHealthStatus: use
    MonthlyDashboardResponse *-- CategorySpending: contain ~List~

    namespace Services{
        class UserService {
            +repo: UserRepository
            +__init__(repo: UserRepository)
            +get_user(user_id: str) UserResponse
            +create_user(user: UserCreate) UserResponse
            +update_user(user_id: str, user: UserUpdate) UserResponse
            +configure_budget(user_id: str, new_income: Optional~float~, new_expenses: Optional~List~FixedExpenseTemplate~) UserResponse
            +update_nutritional_targets(user_id: str, current_weight: float, current_body_fat: float) UserResponse
            -_calculate_tdee(weight_kg: float, height_cm: float, age: int, activity_level: ActivityLevel) float
        }
        class FinanceService {
            +finance_repo: FinanceRepository
            +user_repo: UserRepository
            +__init__(finance_repo: FinanceRepository, user_repo: UserRepository)
            +get_transactions(user_id: str, start_date: date, end_date: date) List~TransactionResponse~
            +add_transaction(user_id: str, transaction: TransactionCreate) TransactionResponse
            +update_transaction(user_id: str, transaction_id: str, transaction: TransactionUpdate) TransactionResponse
            +delete_transaction(user_id: str, transaction_id: str) bool
            +get_monthly_dashboard(user_id: str, month: date) MonthlyDashboardResponse
            -_calculate_burn_rate(user_id: str, actual_date: date) float
            -_calculate_health_status(spent: float, total_budget: float) FinancialHealthStatus
            -_get_category_breakdown(user_id: str, month: date, limit: Optional~int~) List~CategorySpending~
            -_project_savings(income: float, current_spent: float, fixed_expenses: float, date: date) float
            -_get_remaining_days(actual_date: date) int
        }
        class HealthService {
            +nutrition_repo: NutritionRepository
            +biometric_repo: BiometricsRepository
            +user_repo: UserRepository
            +__init__(nutrition_repo: NutritionRepository, biometric_repo: BiometricsRepository, user_repo: UserRepository)
            +get_daily_logs(user_id: str, start_date: date, end_date: date) List~DailyLogResponse~
            +add_daily_log(user_id: str, daily_log: DailyLogCreate) DailyLogResponse
            +update_daily_log(user_id: str, daily_log_id: str, daily_log: DailyLogUpdate) DailyLogResponse
            +delete_daily_log(user_id: str, daily_log_id: str) bool
            +get_biometrics(user_id: str, start_date: date, end_date: date) List~BiometricsResponse~
            +add_biometrics(user_id: str, biometrics: BiometricsCreate) BiometricsResponse
            +update_biometrics(user_id: str, biometrics_id: str, biometrics: BiometricsUpdate) BiometricsResponse
            +delete_biometrics(user_id: str, biometrics_id: str) bool
            +get_health_dashboard(user_id: str, date: date) HealthDashboardResponse
            -_get_macro_summary(user_id: str, actual_date: date) MacroStatus
            -_calculate_overall_loss(user_id: str, actual_date:date) float
            -_calculate_overall_weekly_calories(user_id: str, actual_date:date) float
            -_calculate_days_meeting_goals(user_id: str, actual_date:date) int
            -_calculate_body_fat_pct(waist: float, neck: float, height: float) float
            -_calculate_lean_mass(weight: float, body_fat_pct: float) float
        }
        class IntelligenceService {
            <<External>>
            +api_key:str
            +__init__(api_key:str)
            +parse_transaction(text:str) TransactionCreate
            +parse_food_entry(text:str) List~FoodItem~
        }
    }
    IntelligenceService ..> TransactionCreate : returns
    IntelligenceService ..> FoodItem : returns
    IntelligenceService ..> TransactionCategory : use
    UserService --> UserRepository : use
    UserService ..> UserResponse : returns
    UserService ..> UserCreate : use
    UserService ..> UserUpdate : use
    UserService ..> ActivityLevel : use
    UserService ..> FixedExpenseTemplate : use
    UserService ..> GoalStrategy : use
    FinanceService --> FinanceRepository : use
    FinanceService --> UserRepository : use
    FinanceService ..> TransactionCreate : use
    FinanceService ..> TransactionUpdate : use
    FinanceService ..> TransactionResponse : returns
    FinanceService ..> MonthlyDashboardResponse : returns
    FinanceService ..> CategorySpending : returns
    FinanceService ..> FinancialHealthStatus : returns
    FinanceService ..> TransactionCategory : use
    HealthService --> NutritionRepository : use
    HealthService --> BiometricsRepository : use
    HealthService --> UserRepository : use
    HealthService ..> DailyLogCreate : use
    HealthService ..> DailyLogUpdate : use
    HealthService ..> DailyLogResponse : returns
    HealthService ..> BiometricsCreate : use
    HealthService ..> BiometricsUpdate : use
    HealthService ..> BiometricsResponse : returns
    HealthService ..> HealthDashboardResponse : returns
    HealthService ..> MacroStatus : returns
    namespace Routers{
        class AuthRouter {
            +user_service: UserService
            +__init__(user_service: UserService)
            %% POST /auth/register
            +register(user: UserCreate) UserResponse
            %% POST /auth/login
            +login(token: str) UserResponse
        }
        class UserRouter {
            +user_service: UserService
            +__init__(user_service: UserService)
            %% GET /users/me
            +get_current_user(token: str) UserResponse
            %% PATCH /users/me
            +update_profile(token: str, data: UserUpdate) UserResponse
            %% POST /users/me/config/budget
            +set_budget_config(token: str, income: float, expenses: List~FixedExpenseTemplate~) UserResponse
            %% POST /users/me/config/targets
            +set_nutritional_targets(token: str, weight: float, body_fat: float) UserResponse
        }
        class FinanceRouter {
            +finance_service: FinanceService
            +ai_service: IntelligenceService
            +__init__(f_service, ai_service)
            %% POST /finance/transactions/parse
            +parse_transaction_text(token: str, text: str) TransactionCreate
            %% POST /finance/transactions
            +create_transaction(token: str, transaction: TransactionCreate) TransactionResponse
            %% GET /finance/dashboard
            +get_dashboard(token: str, month: date) MonthlyDashboardResponse
            %% DELETE /finance/transactions/{id}
            +delete_transaction(token: str, tx_id: str) Response
        }
        class HealthRouter {
            +health_service: HealthService
            +ai_service: IntelligenceService
            +__init__(h_service, ai_service)
            %% POST /health/nutrition/parse
            +parse_meal_text(token: str, text: str) List~FoodItem~
            %% POST /health/nutrition/log
            +log_meal(token: str, items: List~FoodItem~) DailyLogResponse
            %% POST /health/biometrics
            +record_biometrics(token: str, data: BiometricsCreate) BiometricsResponse
            %% GET /health/dashboard
            +get_dashboard(token: str, date: date) HealthDashboardResponse
        }
    }
    AuthRouter --> UserService : use
    AuthRouter ..> UserCreate : use
    AuthRouter ..> UserResponse : returns
    UserRouter --> UserService : calls
    UserRouter ..> UserResponse : returns
    UserRouter ..> UserUpdate : use
    UserRouter ..> FixedExpenseTemplate : use
    FinanceRouter --> FinanceService : calls
    FinanceRouter --> IntelligenceService : calls
    FinanceRouter ..> TransactionCreate : use
    FinanceRouter ..> TransactionResponse : returns
    FinanceRouter ..> MonthlyDashboardResponse : returns
    HealthRouter --> HealthService : calls
    HealthRouter --> IntelligenceService : calls
    HealthRouter ..> FoodItem : returns
    HealthRouter ..> DailyLogResponse : returns
    HealthRouter ..> BiometricsCreate : use
    HealthRouter ..> BiometricsResponse : returns
    HealthRouter ..> HealthDashboardResponse : returns
```