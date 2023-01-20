import sqlite3


def dbscores_initialize() -> sqlite3.Connection:
    db = sqlite3.connect("db/scores.sqlite")
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS scores(login TEXT, bestscore INT)"""
    )

    return db


def dbscores_get_best(user_name: str) -> int:
    """Возвращает лучший результат пользователя. Если пользователя нет в базе, то возвращается -1.

    Args:
        user_name (str): Имя пользователя.

    Returns:
        int: Лучший результат пользователя или -1.
    """
    cur = db_scores.cursor()
    inf = cur.execute(
        f"SELECT bestscore from scores where login='{user_name}'").fetchone()
    if inf is None:
        return -1
    return inf[0]


def dbscores_put_current(user_name: str, score: int) -> None:
    """Сохраняет текущий результат пользователя в базу данных. Если пользователя в базе нет, то он создаётся.

    Args:
        user_name (str): Имя пользователя.
        score (int): Текущий результат пользователя.
    """
    cur = db_scores.cursor()
    inf = cur.execute(
        f"SELECT bestscore from scores where login='{user_name}'").fetchone()

    if inf is None:
        cur.execute("INSERT INTO scores (login, bestscore) VALUES(?, ?)", (user_name, score))
    else:
        cur.execute(f"UPDATE scores SET bestscore={score} where login='{user_name}'")
    db_scores.commit()


db_scores: sqlite3.Connection = dbscores_initialize()
