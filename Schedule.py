# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:57:35 2019

@author: THINK
"""
from api import app
from xundaili import Tester
from multiprocessing import Process

class Scheduel():
    def scheduel_test(self):
        test = Tester()
        while True:
            test.run()
        
    def scheduel_api(self):
        while True:
            app.run()
        
    def run(self):
        task1 = Process(target=self.scheduel_test)
        task1.start()
        
        task2 = Process(target=self.scheduel_api)
        task2.start()
        
if __name__ == '__main__':
    schedule = Scheduel()
    schedule.run()