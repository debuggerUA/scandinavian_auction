# encoding: utf-8

from psycopg2 import connect
from os import system
import datetime, time
import threading
from time import sleep

work = True

def endAuction(id, conn, curr):
    querry = 'SELECT id, user_id, auction_id FROM auction_bid WHERE auction_id=' + id + ' ORDER BY id'
    curr.execute(querry)
    rows = curr.fetchall()
    

class dbThread(threading.Thread):
    def run(self):
        conn = connect("dbname=AuctionDB user=auction password=auction")
        curr = conn.cursor()
        while work:
            querry = 'SELECT id, time_left FROM auction_auction WHERE is_active=TRUE'
            curr.execute(querry)
            rows = curr.fetchall()
            for row in rows:
                time_left_sec = row[1].hour*3600 + row[1].minute*60 + row[1].second
                if time_left_sec > 0:
                    time_left_sec -= 1
                    new_time_left = datetime.time(time_left_sec/3600, (time_left_sec % 3600)/60, time_left_sec % 60)
                    curr.execute('UPDATE auction_auction SET time_left=%s WHERE id=%s', (new_time_left, row[0]))
                    conn.commit()
                else:
                    curr.execute('UPDATE auction_auction SET is_active=FALSE WHERE id=%s', (row[0],))
                    conn.commit()
                    endAuction(row[0], conn, curr)
            sleep(1)


class djangoThread(threading.Thread):
    def run(self):
        system("python manage.py runserver")


def _main():
    dbThread().start()
    djangoThread().start()
    

if __name__ == '__main__':
    _main()