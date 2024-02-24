from battle_stat import db_session
from battle_stat.model.dim_move import MoveDimension


def get_all_dim_moves():
    return db_session.query(MoveDimension).all()


def get_dim_move_by_name(move_name):
    return db_session.query(MoveDimension).filter(MoveDimension.name == move_name).first()
