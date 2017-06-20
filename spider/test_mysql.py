import sys
import unittest
import pymysql.cursors


class PythonMySQL(unittest.TestCase):
    def test_connect(self):
        print('sys.path: ' + str(sys.path))
        print('module pymysql: ')
        print(dir(pymysql))

        conn = pymysql.connect('localhost', 'root', 'password', 'spider')
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("Database version : %s " % data)

        conn.close()

if __name__ == '__main__':
    unittest.main()

