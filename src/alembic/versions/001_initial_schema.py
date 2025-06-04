"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-05-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE "Users" (
            id SERIAL PRIMARY KEY NOT NULL UNIQUE,
            login VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR NULL UNIQUE,
            name VARCHAR NULL,
            surname VARCHAR NULL,
            patronymic VARCHAR NULL,
            password VARCHAR NOT NULL,
            input_tokens INTEGER NULL,
            output_tokens INTEGER NULL
        );

        CREATE TABLE "AIInfo" (
            id SERIAL PRIMARY KEY NOT NULL UNIQUE,
            system_prompt VARCHAR NULL,
            temperature DOUBLE PRECISION NOT NULL DEFAULT 0.7,
            top_p DOUBLE PRECISION NOT NULL DEFAULT 0.8,
            stream BOOLEAN DEFAULT false,
            model VARCHAR NOT NULL
        );

        CREATE TABLE "Chat" (
            id SERIAL PRIMARY KEY NOT NULL UNIQUE,
            title VARCHAR(100) NOT NULL,
            ai_config_id INTEGER NOT NULL,
            FOREIGN KEY (ai_config_id) REFERENCES "AIInfo" (id)
        );

        CREATE TABLE "ChatHistory" (
            id SERIAL PRIMARY KEY NOT NULL UNIQUE,
            message VARCHAR NOT NULL,
            author_id INTEGER NULL,
            chat_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES "Users" (id),
            FOREIGN KEY (chat_id) REFERENCES "Chat" (id)
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS "ChatHistory";
        DROP TABLE IF EXISTS "Chat";
        DROP TABLE IF EXISTS "AIInfo";
        DROP TABLE IF EXISTS "Users";
        DROP TABLE IF EXISTS "FullName";
        """
    )