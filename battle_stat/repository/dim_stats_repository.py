from battle_stat import db_session
from battle_stat.model.dim_move import MoveDimension
from battle_stat.model.dim_stats import StatDimension
from model.move import Move


def get_all_dim_stats():
    return db_session.query(StatDimension).all()


def get_dim_stat_by_type_name(stat_type, move_name):
    return db_session.query(StatDimension).join(MoveDimension).filter(
        StatDimension.name == stat_type).filter(
        MoveDimension.name == move_name).first()
