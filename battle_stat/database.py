from battle_stat import db_session


def save_data(data):
    """Add information to the session and commit it in the DB

    :param data:The data object/objects that will be saved."""
    try:
        db_session.add(data)
        db_session.commit()
    except:
        db_session.rollback()
        raise


def save_list_data(data):
    """Add information to the session and commit it in the DB

    :param data:The data object/objects that will be saved."""
    try:
        if data:
            for obj in data:
                db_session.add(obj)
            db_session.commit()
    except:
        db_session.rollback()
        raise


def delete_data(data):
    """Delete data from the DB.

    :param data:The data object that will be deleted."""
    try:
        db_session.delete(data)
        db_session.commit()
    except:
        db_session.rollback()
        raise


def list_data_for_deletion(data):
    """Add information to the session without committing it in the DB

    :param data:The data object/objects that will be deleted."""
    try:
        if data:
            for obj in data:
                if obj:
                    db_session.delete(obj)
    except:
        db_session.rollback()
        raise


def list_data_for_saving(data):
    """Add information to the session without committing it in the DB

    :param data:The data object/objects that will be saved."""
    try:
        if data:
            for obj in data:
                db_session.add(obj)
    except:
        db_session.rollback()
        raise


def flush_and_commit_changes():
    """Flushes all changed objects from the session and commits the changes."""
    try:
        db_session.flush()
        db_session.commit()
    except:
        db_session.rollback()
        raise


def flush():
    """Flushes all changes from the session without committing."""
    try:
        db_session.flush()
        db_session.rollback()
    except:
        db_session.rollback()
        raise


def rollback_and_close():
    """Flushes all changes from the session without committing."""
    try:
        db_session.rollback()
    except:
        raise
    finally:
        db_session.close()

