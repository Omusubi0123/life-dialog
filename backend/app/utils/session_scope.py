from contextlib import contextmanager


@contextmanager
def session_scope(session):
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
