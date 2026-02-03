**Alembic**
1. Autogenerate
alembic revision --autogenerate -m "add users table"

2. Upgrade / Downgrade
alembic upgrade head
alembic downgrade -1

3. Apply migration
alembic upgrade head

4. Initialize migration
alembic upgrade head