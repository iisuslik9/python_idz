"""sql init tables

Revision ID: e81b35e92b15
Revises: 23d4af767c54
Create Date: 2026-05-20 14:51:18.022453

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e81b35e92b15'
down_revision: Union[str, Sequence[str], None] = '23d4af767c54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""
    CREATE TABLE warehouse (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL,
        capacity FLOAT NOT NULL
    );
    CREATE TABLE shipment (
        id SERIAL PRIMARY KEY,
        tracking_number VARCHAR(255) UNIQUE NOT NULL,
        weight FLOAT NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'на складе',
        warehouse_id INTEGER NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE
    );
    CREATE TABLE driver (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        license_number VARCHAR(255) UNIQUE NOT NULL
    );
    CREATE TABLE shipment_driver (
        id SERIAL PRIMARY KEY,
        shipment_id INTEGER NOT NULL REFERENCES shipment(id) ON DELETE CASCADE,
        driver_id INTEGER NOT NULL REFERENCES driver(id) ON DELETE CASCADE,
        delivery_date DATE NOT NULL
    );
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS shipment_driver;
    DROP TABLE IF EXISTS shipment;
    DROP TABLE IF EXISTS warehouse;
    DROP TABLE IF EXISTS driver;
    """)
