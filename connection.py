import pymysql
import pymysql.cursors as cursors

from domain_class import Domain


class MysqlConnection:
    def __init__(self, host, user, password, db):
        self.connection = self.get_connection(host, user, password, db)

    def get_domain_object_list(self):
        sql = "select * from domain"
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        domains = [Domain(**obj) for obj in cursor.fetchall()]
        return domains

    def get_crawled_urls_by_domain_id(self, domain_id):
        sql = "select url from domain_url where domain_id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (domain_id,))
        urls = [url['url'] for url in cursor.fetchall()]
        return urls

    def insert_domain(self, domain_name):
        sql = "insert into domain (domain_name) values (%s)"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (domain_name,))
        self.connection.commit()

    def insert_domains(self, domain_names):
        sql = "insert into domain (domain_name) values (%s)"
        with self.connection.cursor() as cursor:
            cursor.executemany(sql, [(domain_name,) for domain_name in domain_names])
        self.connection.commit()

    def update_domain_object(self, domain):
        sql = "insert into domain_url (domain_id, url) values (%s, %s)"
        with self.connection.cursor() as cursor:
            cursor.executemany(sql, [(domain.domain_id, url) for url in domain.new_urls])
        self.connection.commit()

    def get_domain_object_by_domain_id(self, domain_id):
        select_domain_name_sql = "select domain_name from domain where domain_id = %s"
        select_crawled_urls_sql = "select url from domain_url where domain_id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(select_domain_name_sql, (domain_id,))
            domain_name = cursor.fetchone().get('domain_name')

            cursor.execute(select_crawled_urls_sql, (domain_id,))
            crawled_urls = [url['url'] for url in cursor.fetchall()]
        return Domain(domain_name=domain_name, crawled_urls=crawled_urls, domain_id=domain_id)

    def get_domain_id_list(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select domain_id from domain")
            domain_ids = [obj['domain_id'] for obj in cursor.fetchall()]
        return domain_ids

    def close_connection(self):
        self.connection.close()

    @staticmethod
    def get_connection(host, user, password, db):
        try:
            connection = pymysql.connect(host=host, user=user, password=password, db=db, charset="utf8",
                                         cursorclass=cursors.DictCursor)
            return connection
        except Exception:
            print("Can't connect to the database")
            return None
