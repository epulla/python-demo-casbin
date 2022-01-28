from .db_engine import DBEngine

# Users
def get_user_by_id(engine: DBEngine, id: int):
    return [x for x in engine.execute_query(f'SELECT * FROM user WHERE id={id}')][0]