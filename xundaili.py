VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100

import aiohttp
import redis
from random import choice
import asyncio
import time

class Redis():
    def __init__(self):
        self.db = redis.StrictRedis(host='114.116.123.62',port=6379)
    
    def decrease(self,proxy):
        score = self.db.zscore('proxies',proxy)
        if 0 < score <=100:
            print('当前分数：',score,'减1')
            self.db.zincrby('proxies',proxy,-1)
        else:
            self.db.zrem('proxies',proxy)
    
    def random(self):
        result = self.db.zrangebyscore('proxies',100,100)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange('proxies',0,100)
            if len(result):
                return choice(result)
                print('dsfs')
            else:
                raise
    
    def all(self):
        return self.db.zrangebyscore('proxies',0,100)
    
    def maxi(self, proxy):
        self.db.zadd('proxies', 100, proxy)
    

class Tester(object):
    def __init__(self):
        self.db = Redis()
    
    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                print('正在测试')
                async with session.get(TEST_URL, proxy=proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.db.maxi(proxy)
                        print('代理可用')
                    else:
                        print('请求响应码不合法')
                        self.db.decrease(proxy)
            except ( TimeoutError, AttributeError):
                self.db.decrease(proxy)
                print('代理请求失败')
                
    def run(self):
        print('测试器开始运行')
        try:
            proxies = self.db.all()
            for i in range(0,len(proxies),100):
                loop = asyncio.get_event_loop()
                test_proxies = proxies[i:i+100]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('服务器发生错误:',e)




