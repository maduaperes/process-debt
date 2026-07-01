from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================
# 2. Schema de Cadastro (Request Body)
# ==========================================
class UserCreate(BaseModel):
    """
    Schema utilizado para a criação de um novo usuário.
    Validações aplicadas:
    - name: Obrigatório, entre 3 e 150 caracteres.
    - email: Obrigatório, precisa ser um formato de e-mail válido.
    - password: Obrigatório, mínimo de 8 e máximo de 128 caracteres.
    """
    name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


# ==========================================
# 3. Schema de Login (Autenticação)
# ==========================================
class UserLogin(BaseModel):
    """Schema utilizado para receber as credenciais no endpoint de login."""
    email: EmailStr
    password: str


# ==========================================
# 4. Schema de Resposta (Response Body)
# ==========================================
class UserResponse(BaseModel):
    """
    Schema utilizado para retornar os dados do usuário de forma segura.
    Garante que o hash da senha NUNCA vaze na API.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str


# ==========================================
# 5. Schemas do JWT (Tokens de Acesso)
# ==========================================
class Token(BaseModel):
    """Retornado após um login bem-sucedido."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Utilizado internamente para carregar os dados contidos dentro do token extraído."""
    email: str | None = None