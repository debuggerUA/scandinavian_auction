# encoding: utf-8

from psycopg2 import connect
from os import system
import datetime, time
import threading
from time import sleep


work = True


try:
    conn = connect(database="AuctionDB", user="auction", password="auction")
    curr = conn.cursor()
except:
    print "Database connection Error!"
    work = False


def endAuction(id, conn, curr): 
    curr.execute("SELECT id, user_id FROM auction_bid WHERE auction_id=%s ORDER BY id DESC", (id,))
    bid_row = curr.fetchone()
    print bid_row[0]
    curr.execute("UPDATE auction_auction SET won_by_id=%s WHERE id=%s", (bid_row[1], id))
    conn.commit()
    print "Auction ended."

class dbThread(threading.Thread):
    def run(self):
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
        system("python manage.py runserver 8000")

class tornadoThread(threading.Thread):
    def run(self):
        system("python tornading.py")


def _main():
    dbThread().start()
    tornadoThread().start()
    djangoThread().start()


if __name__ == '__main__':
    _main()