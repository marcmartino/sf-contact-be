import pymysql
import falcon
from falcon_cors import CORS
from .contacts import Collection, Item

cors = CORS(allow_origins_list=['http://sf-contacts.now.sh', 'https://sf-contacts.now.sh', 'http://localhost:8080'],
            allow_all_headers=True,
            allow_all_methods=True)

api = application = falcon.API(middleware=[cors.middleware])

connection = pymysql.connect(host='sql3.freesqldatabase.com',
                             user='sql3185494',
                             password='2pUBwD6jvP',
                             db='sql3185494',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

contacts_collection = Collection(connection)
contacts_item = Item(connection)
api.add_route('/contacts', contacts_collection)
api.add_route('/contacts/{id}', contacts_item)