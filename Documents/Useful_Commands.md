**Alembic**
1. Initiate Migration:
alembic init migration

2. Autogenerate
alembic revision --autogenerate -m "add users table"

3. Upgrade / Downgrade
alembic upgrade head
alembic downgrade -1

4. Apply migration
alembic upgrade head

5. Initialize migration
alembic upgrade head