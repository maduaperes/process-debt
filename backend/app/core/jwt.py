from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings

# ==========================================
# 1. Função para Geração do Token JWT
# ==========================================
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Cria um JSON Web Token (JWT) assinado.
    
    Insere uma data de expiração (exp) no payload do token com base
    nas configurações do sistema ou no delta informado manualmente.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


# ==========================================
# 2. Função para Validação e Decodificação
# ==========================================
def decode_access_token(token: str) -> dict:
    """
    Valida a assinatura de um JWT, checa a expiração e retorna seu payload.
    
    Lança ValueError caso o token seja inválido, adulterado ou tenha expirado.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError:
        raise ValueError("Token inválido ou expirado.")