import json
import falcon

#class ContactModel():
#
#    def __init__(self, json_obj):
#        self.first_name = json_obj['first_name'] or ''
#        self.last_name = json_obj['last_name'] or ''
#        self.picture_url = json_obj['picture_url'] or ''
#        self.date_of_birth = json_obj['date_of_birth'] or ''
#        self.phone_number = json_obj['phone_number'] or ''
#        self.zip_code = json_obj['zip_code'] or ''
#        self.starred = json_obj['starred'] or 0

class Collection(object):

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def on_get(self, req, resp):
        try:
            with self.db_conn.cursor() as cursor:
                order_by = req.get_param('order') or 'id'
                sql = "SELECT `id`, `first_name`, `last_name`, `picture_url`, `date_of_birth`, `phone_number`, `zip_code`, `starred`, `note` FROM `contact` ORDER BY %s"
                cursor.execute(sql, (order_by))
                result = cursor.fetchall()
                resp.body = json.dumps(result, ensure_ascii=False)
                resp.status = falcon.HTTP_200
        except:
            resp.body = json.dumps({
                    'message': 'issue retrieving your contact'
                }, ensure_ascii=False)
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):
        post_body = json.loads(req.stream.read())
        try:
            with self.db_conn.cursor() as cursor:
                sql = "INSERT INTO `contact` (`first_name`, `last_name`, `picture_url`, `date_of_birth`, `phone_number`, `zip_code`, `note`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, args=(post_body['first_name'] or '', post_body['last_name'] or '', post_body['picture_url'] or '', post_body['date_of_birth'] or '', post_body['phone_number'] or 0, int(post_body['zip_code']) or 0, post_body['note'] or ''))
                self.db_conn.commit()
                resp.body = json.dumps({'message': 'created', 'id': cursor.lastrowid}, ensure_ascii=False)
                resp.status = falcon.HTTP_200
        except:
            resp.body = json.dumps({
                    'message': 'issue retrieving your contact'
                }, ensure_ascii=False)
            resp.status = falcon.HTTP_500

class Item(object):

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def on_get(self, req, resp, id):
        try:
            with self.db_conn.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `first_name`, `last_name`, `picture_url`, `date_of_birth`, `phone_number`, `zip_code`, `starred`, `note` FROM `contact` WHERE `id`=%s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                resp.body = json.dumps(result, ensure_ascii=False)
                resp.status = falcon.HTTP_200
        except:
            resp.body = json.dumps({
                    'message': 'issue retrieving your contact'
                }, ensure_ascii=False)
            resp.status = falcon.HTTP_500

    def on_put(self, req, resp, id):
        post_body = json.loads(req.stream.read())
        try:
            with self.db_conn.cursor() as cursor:
                sql = "UPDATE `contact` SET `first_name`=%s, `last_name`=%s, `picture_url`=%s, `date_of_birth`=%s, `phone_number`=%s, `zip_code`=%s, `note`=%s WHERE `id`=%s"
                cursor.execute(sql, (post_body['first_name'] or '', post_body['last_name'] or '', post_body['picture_url'] or '', post_body['date_of_birth'] or '', post_body['phone_number'] or 0, int(post_body['zip_code']) or 0, post_body['note'] or '', id))

            self.db_conn.commit()
            resp.body = json.dumps({'message': 'updated'}, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except:
            resp.body = json.dumps({
                    'message': 'issue retrieving your contact'
                }, ensure_ascii=False)
            resp.status = falcon.HTTP_500