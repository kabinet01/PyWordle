import sqlite3


def connect_db():
    """Connect to the database

    Returns:
        sqlite3.Connection: Returns the sqlite3 database connection
    """
    conn = sqlite3.connect('user.db')
    return conn


def initialize_database():
    """Initialize the database
    """
    conn = connect_db()
    cur = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS user
            (name TEXT UNIQUE PRIMARY KEY,
            password TEXT,
            score INT)
    '''
    cur.execute(query)
    conn.close()


def register_user(name, password, score):
    """Register a user and insert it into the database

    Args:
        name (string): user name
        password (string): password hash
        score (int): score

    Returns:
        bool: Return true is register successfully, else return false
    """
    try:
        conn = connect_db()
        cur = conn.cursor()
        data_tuple = (name, password, score)
        query = '''INSERT INTO user (name, password, score)
                VALUES (?, ?, ?)'''
        cur.execute(query, data_tuple)
        conn.commit()
        conn.close()
        
    except sqlite3.IntegrityError:
        return False
    
    return True


def login_user(name, password):
    """Authenticate a user based on provided credentials.

    Args:
        name (str): The username of the user
        password (str): The password hash of the user

    Returns:
        bool: True if the provided credentials match an entry in the database, False otherwise.

    """
    conn = connect_db()
    cur = conn.cursor()
    data_tuple = (name, password)
    query = '''SELECT * FROM user WHERE name = ? AND password = ?'''
    cur.execute(query, data_tuple)
    res = cur.fetchone()
    conn.close()
    if res:
        return True
    return False


def get_score(name):
    """Get the score of the user

    Args:
        name (string): User name

    Returns:
        int: score of the user
    """
    conn = connect_db()
    cur = conn.cursor()
    data_tuple = (name,)
    query = '''SELECT score FROM user WHERE name = ?'''
    cur.execute(query, data_tuple)
    res = cur.fetchone()
    conn.close()
    if res:
        return res[0]


def change_score(name, score):
    """Update the score of the user

    Args:
        name (string): User name
        score (int): new score of the user
    """
    conn = connect_db()
    cur = conn.cursor()
    data_tuple = (score, name)
    query = '''UPDATE user SET SCORE = ? WHERE NAME = ?'''
    cur.execute(query, data_tuple)
    conn.commit()
    conn.close()


def get_leaderboard():
    """Get the leaderboard

    Returns:
        list: Return a list of player in the database, along with their score. Limit to 10
    """
    conn = connect_db()
    cur = conn.cursor()
    query = '''SELECT name, score FROM user LIMIT 10'''
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows
