"""add super_user

Revision ID: 65ad5d6e496c
Revises: adb793fcae04
Create Date: 2024-08-19 14:15:18.271591

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import bcrypt

from src.config import CONFIG

# revision identifiers, used by Alembic.
revision: str = "65ad5d6e496c"
down_revision: Union[str, None] = "adb793fcae04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the hashed password for the superuser
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def upgrade() -> None:
    # Insert a super user into the users table
    superuser_email = CONFIG.SUPERUSER_EMAIL
    superuser_name = CONFIG.SUPERUSER_NAME
    superuser_password = CONFIG.SUPERUSER_PASSWORD  # Replace with your actual secure password
    hashed_password = hash_password(superuser_password)

    op.bulk_insert(
        sa.table(
            'users',
            sa.column('id', sa.Integer),
            sa.column('hashed_password', sa.LargeBinary),
            sa.column('email', sa.String(32)),
            sa.column('name', sa.String(16)),
            sa.column('is_admin', sa.Boolean),
        ),
        [
            {
                'id': 1,  # Ensure the id is unique and does not conflict with existing ids
                'hashed_password': hashed_password,
                'email': superuser_email,
                'name': superuser_name,
                'is_admin': True
            }
        ]
    )


def downgrade() -> None:
    # Remove the super user from the users table
    op.execute(
        sa.text("DELETE FROM users WHERE email = :email").bindparams(email="superuser@example.com")
    )
