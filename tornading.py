import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from psycopg2 import connect

import datetime, time
from django.utils import simplejson

define("port", default=8001, help="run on the given port", type=int)

work = True

class AJAXHandler(tornado.web.RequestHandler):
    def get(self):
        querry = 'SELECT id, time_left, price, product_id FROM auction_auction WHERE is_active=TRUE ORDER BY id'
        curr.execute(querry)
        auc_rows = curr.fetchall()
        id_hash_sum = 0
        time_left_array = []
        prices_array = []
        products_array = []
        for auc in auc_rows:
            id_hash_sum += auc[0]
            time_left_array.append(auc[1].__str__())
            prices_array.append(auc[2])
            curr.execute('SELECT name FROM products_product WHERE id=%s', (auc[3],))
            pr_row = curr.fetchall()
            products_array.append(pr_row[0][0])
        data = {}
        data.update({'id_hash_sum': id_hash_sum, 'products_array': products_array, 'time_left_array': time_left_array, 'prices_array': prices_array, 'success': True})
        self.write(simplejson.dumps(data))


def main():
    if(work):
        tornado.options.parse_command_line()
        application = tornado.web.Application([(r"/", AJAXHandler),])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    else:
        print "can't start"


if __name__ == "__main__":
    try:
        conn = connect(database="AuctionDB", user="auction", password="auction")
        curr = conn.cursor()
    except:
        print "Database connection Error!"
        work = False
    main()