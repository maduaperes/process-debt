from datetime import timedelta

from app.core.config import settings
from app.core.jwt import create_access_token
from app.core.password import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        """Recebe a dependência do UserRepository pelo construtor."""
        self.repository = repository

    # ==========================================
    # 4 a 7. Cadastro de Usuário
    # ==========================================
    def create_user(self, user_data: UserCreate) -> User:
        """
        Executa a regra de negócio para cadastrar um novo usuário.
        Verifica duplicidade de e-mail e aplica hash criptográfico na senha.
        """
        # Verifica se o e-mail já está em uso
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Já existe um usuário com esse e-mail.")

        # Cria a instância do modelo injetando o hash seguro da senha
        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        return self.repository.create(user)

    # ==========================================
    # 8 e 9. Autenticação (Login)
    # ==========================================
    def authenticate_user(self, email: str, password: str) -> User:
        """
        Valida as credenciais do usuário.
        Retorna uma mensagem genérica em caso de falha por segurança.
        """
        user = self.repository.get_by_email(email)

        # Se o usuário não existir, encerra com erro genérico
        if user is None:
            raise ValueError("E-mail ou senha inválidos.")

        # Se a senha informada for incompatível com o hash, encerra com o mesmo erro genérico
        if not verify_password(password, user.password_hash):
            raise ValueError("E-mail ou senha inválidos.")

        return user

    # ==========================================
    # 10. Geração do Token JWT
    # ==========================================
    def create_token(self, user: User) -> Token:
        """Gera um token de acesso baseado no e-mail do usuário autenticado."""
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(
                minutes=settings.access_token_expire_minutes
            ),
        )

        return Token(access_token=access_token)

    # ==========================================
    # 11. Busca de Usuário por ID
    # ==========================================
    def get_user_by_id(self, user_id: int) -> User:
        """Busca uma entidade de usuário pelo ID e lança exceção se não existir."""
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise ValueError("Usuário não encontrado.")
        
        return user