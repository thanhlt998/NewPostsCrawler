import redis


class RedisServer:
    def __init__(self, host, port, db):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.redis_server = redis.Redis(connection_pool=pool)

    def get_redis_db(self):
        return self.redis_server

    def set_no_spiders(self, no_spiders):
        return self.redis_server.set("no_spiders", no_spiders)

    def get_no_spiders(self):
        return int(self.redis_server.get("no_spiders"))

    def increase_no_spiders(self):
        return self.redis_server.incr("no_spiders", 1)

    def decrease_no_spiders(self):
        return self.redis_server.decr("no_spiders", 1)

    def insert_domain(self, key_name, domain):
        return self.redis_server.lpush(key_name, domain)

    def remove_domains(self, key_name, domains):
        no_current_domains = self.get_no_domains()
        removed_domains = []
        i = 0

        while i < no_current_domains:
            domain = int(self.pop_domain(key_name))
            if domain in domains:
                removed_domains.append(domain)
            else:
                self.insert_domain(key_name, domain)
            i += 1

        self.set_no_domains(no_current_domains - len(removed_domains))

    def set_no_domains(self, no_domains):
        self.redis_server.set('no_domains', no_domains)

    def get_no_domains(self):
        no_domains = self.redis_server.get('no_domains')
        return int(no_domains) if no_domains else 0

    def pop_domain(self, key_name):
        return self.redis_server.rpop(key_name)

    def get_domains_to_crawl(self, key_name):
        domain = self.redis_server.rpop(key_name)
        self.redis_server.lpush(key_name, domain)
        return domain

    def clear_all_keys(self):
        for key in self.redis_server.keys():
            self.redis_server.delete(key)

    def clear_key_list(self, key_list):
        for key in key_list:
            self.redis_server.delete(key)

    def clear_key(self, key_name):
        self.redis_server.delete(key_name)

    def set_default_values(self):
        self.redis_server.set("no_spiders", 0)

    def set_list(self, list_name, list_val):
        self.clear_key(key_name=list_name)
        for obj in list_val:
            self.redis_server.lpush(list_name, obj)
