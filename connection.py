import pymysql
import pymysql.cursors as cursors

from domain_class import Domain
from utils import get_time_before_now, get_time_now
from settings.domain_crawler_settings import EXPIRE_WINDOWS_TIME_SIZE


class MysqlConnection:
    def __init__(self, host, user, password, db):
        self.connection = self.get_connection(host, user, password, db)

    def get_domain_object_list(self):
        sql = "select domain_id, domain_name from domain"
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
        sql = f"insert into domain_url (domain_id, url, crawl_time) values (%s, %s, '{get_time_now()}')"
        with self.connection.cursor() as cursor:
            cursor.executemany(sql, [(domain.domain_id, url) for url in domain.new_urls])
        self.connection.commit()

    def get_domain_object_by_domain_id(self, domain_id):
        select_domain_name_sql = "select domain_name from domain where domain_id = %s"
        select_crawled_urls_sql = f"select url from domain_url where domain_id = %s" \
            f" and crawl_time > '{get_time_before_now(EXPIRE_WINDOWS_TIME_SIZE)}'"
        with self.connection.cursor() as cursor:
            cursor.execute(select_domain_name_sql, (domain_id,))
            domain_name = cursor.fetchone().get('domain_name')

            cursor.execute(select_crawled_urls_sql, (domain_id,))
            crawled_urls = [url['url'] for url in cursor.fetchall()]
        return Domain(domain_name=domain_name, crawled_urls=crawled_urls, domain_id=domain_id)

    def insert_new_domain(self, domain_name):
        insert_domain_sql = "insert into domain (domain_name, " \
                            "first_time_crawl," \
                            "last_time_updated," \
                            "domain_age," \
                            "domain_popularity," \
                            "error_rate," \
                            "avg_request_time," \
                            "avg_new_posts_per_day," \
                            "no_requested_requests," \
                            "no_out_domains," \
                            "pagerank," \
                            "ssl_grade," \
                            "meaning_word_rate," \
                            "no_sub_domains," \
                            "domain_length," \
                            "score) values (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)"
        select_id_sql = "select domain_id from domain where domain_name like %s"
        with self.connection.cursor() as cursor:
            cursor.execute(select_id_sql, (domain_name,))
            domain_id = cursor.fetchone()

            if not domain_id:
                cursor.execute(insert_domain_sql, (domain_name,))
                self.connection.commit()
                cursor.execute(select_id_sql, (domain_name,))
                domain_id = cursor.fetchone()['domain_id']

                return domain_id
        return domain_id['domain_id']

    def get_domain_id_list(self, no_domains_limit=None):
        with self.connection.cursor() as cursor:
            cursor.execute("select domain_id from domain order by score" + (
                f" limit {no_domains_limit}" if no_domains_limit else ''))
            domain_ids = [obj['domain_id'] for obj in cursor.fetchall()]
        return domain_ids

    def get_domain_id_list_with_domain_names(self, domains):
        sql = f"select domain_id from domain where domain_name in ({', '.join(['%s'] * len(domains))})"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, tuple(domains))
            domain_ids = [domain['domain_id'] for domain in cursor.fetchall()]

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
