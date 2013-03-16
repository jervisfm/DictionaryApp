__author__ = 'Jervis Muindi'

import sqlite3
import json
import time

DB_NAME = 'words.db'
DB_TABLE = 'words'

def load_json():
    fp = open('words_compiled.txt')
    return json.load(fp)

def db_connect():
    global DB_NAME
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_db_schema():
    global DB_NAME, DB_TABLE
    print 'updating db schema'
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Delete Android MetaData
    drop_android_table = "DROP TABLE IF EXISTS android_metadata"
    c.execute(drop_android_table)

    # Delete Word Table
    drop_word_table = "DROP TABLE IF EXISTS %s" % (DB_TABLE)
    c.execute(drop_word_table)

    # Create Android Meta data
    create_android_table = "CREATE TABLE android_metadata (locale TEXT)"
    c.execute(create_android_table)

    # Create Words Table
    create_word_table = """CREATE TABLE words
                           (_id INTEGER PRIMARY KEY,
                            word text, date text, html text)"""
    c.execute(create_word_table)

    conn.commit()
    conn.close()
    print 'Successfully created/update table schema'

def load_database():
    conn = db_connect()
    c = conn.cursor()
    print 'Loading Words to memory...'
    data = load_json()
    print 'done. proceeding ...'

    global DB_TABLE
    curr_time = time.ctime()
    insert_template = "INSERT INTO %s VALUES(NULL, ?, ?, ?)"

    word_count = len(data)
    print 'Loading %d Words to database' % word_count
    i = 0
    for word in data:
        print 'Processing Word %d of %d - %s' % (i, word_count, word)
        val = data[word]
        content = val['html']
        if len(content) == 0:
            continue
        insert_stmt = insert_template % (DB_TABLE)
        c.execute(insert_stmt, [word, curr_time, content])
        i += 1


    conn.commit()
    conn.close()
    print 'Database Loading Complete'

def test():
    create_db_schema()
    load_database()

def main():
    print 'DB Loader Script for words'
    test()

if __name__ == '__main__':
    main()
