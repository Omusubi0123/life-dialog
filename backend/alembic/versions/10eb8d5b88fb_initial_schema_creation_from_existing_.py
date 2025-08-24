"""Initial schema creation from existing database

Revision ID: 10eb8d5b88fb
Revises: 
Create Date: 2025-08-24 02:42:17.194621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '10eb8d5b88fb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable pgvector extension first
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create users table
    op.create_table('users',
    sa.Column('user_id', sa.String(length=40), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('mode', sa.String(length=10), nullable=True),
    sa.Column('icon_url', sa.Text(), nullable=True),
    sa.Column('status_message', sa.Text(), nullable=True),
    sa.Column('link_token', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    
    # Create analysis table
    op.create_table('analysis',
    sa.Column('analysis_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=40), nullable=True),
    sa.Column('uploaded_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('personality', sa.Text(), nullable=True),
    sa.Column('strength', sa.Text(), nullable=True),
    sa.Column('weakness', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('analysis_id')
    )
    
    # Create diary table
    op.create_table('diary',
    sa.Column('diary_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=40), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('diary_id')
    )
    
    # Create message table
    op.create_table('message',
    sa.Column('message_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('diary_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(length=40), nullable=True),
    sa.Column('media_type', sa.String(length=10), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('sent_at', sa.TIME(), nullable=True),
    sa.ForeignKeyConstraint(['diary_id'], ['diary.diary_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('message_id')
    )
    
    # Create diary_vector table
    op.create_table('diary_vector',
    sa.Column('vector_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=40), nullable=True),
    sa.Column('diary_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('diary_content', sa.Text(), nullable=True),
    sa.Column('diary_vector', Vector(1536), nullable=True),
    sa.ForeignKeyConstraint(['diary_id'], ['diary.diary_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('vector_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order due to foreign key constraints
    op.drop_table('diary_vector')
    op.drop_table('message')
    op.drop_table('diary')
    op.drop_table('analysis')
    op.drop_table('users')
    
    # Note: pgvector extension is not dropped to avoid potential data loss
    # If you really need to drop it, uncomment the following line:
    # op.execute('DROP EXTENSION IF EXISTS vector CASCADE')
