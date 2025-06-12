import sqlite3
import pytest

@pytest.fixture
def sample_db(tmp_path):
    dbfile = tmp_path / "student.db"
    conn = sqlite3.connect(str(dbfile))
    cursor = conn.cursor()
    # create table
    cursor.execute("""
        CREATE TABLE STUDENT(
            NAME TEXT,
            CLASS TEXT,
            SECTION TEXT,
            MARKS INTEGER
        )
    """)
    # insert sample rows
    rows = [
        ('Harsh', 'Data Science', 'A', 90),
        ('John',  'Web Development', 'B', 100),
        ('Mukesh','App Development','A', 86),
        ('Jacob','DEVOPS','A', 50),
        ('Dipesh','DEVOPS','A', 35),
    ]
    cursor.executemany("INSERT INTO STUDENT VALUES (?,?,?,?)", rows)
    conn.commit()
    yield conn
    conn.close()

def query_names_over(cursor, threshold):
    cursor.execute(
        "SELECT NAME FROM STUDENT WHERE MARKS > ? ORDER BY NAME", (threshold,)
    )
    return [row[0] for row in cursor.fetchall()]

def test_query_marks_above_48(sample_db):
    names = query_names_over(sample_db.cursor(), 48)
    assert names == ['Harsh', 'John', 'Mukesh']

def test_no_one_over_120(sample_db):
    names = query_names_over(sample_db.cursor(), 120)
    assert names == []