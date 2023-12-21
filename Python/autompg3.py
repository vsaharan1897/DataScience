#Vishesh Saharan
#HW8
#COMP 3006

import csv
import os
import collections as collect
import logging 
import requests
import argparse
from operator import attrgetter
import matplotlib.pyplot as plot
import numpy as np 
import pandas as pd 



class AutoMPG:
    def __init__(self,make,model,year,mpg):
        self.make=make
        self.model=model
        self.year=year
        self.mpg=mpg
    def __repr__(self) -> str:
        return f"AutoMPG('{self.make}','{self.model}', {self.year}, {self.mpg})"
    def __str__(self) -> str:
        return repr(self)
    def __eq__(self, other: object) -> bool:
         return [self.make, self.model, self.year, self.mpg] == [other.make, other.model, other.year,
                                                                     other.mpg]
    def __lt__(self,other):
        return [self.make, self.model, self.year, self.mpg] < [other.make, other.model, other.year,other.mpg]
    def __hash__(self) -> int:
        return hash((self.make,self.model,self.year,self.mpg))


class AutoMPGData:
    def __init__(self):
        self.iter=0
        self.result=[]
        self._load_data()

    def get_correct_name(self,name):
        if name == 'chevroelt' or name == 'chevy':
            return 'chevrolet'
        elif name == 'maxda':
            return 'mazda'
        elif name == 'mercedes-benz':
            return 'mercedes'
        elif name == 'toyouta':
            return 'toyota'
        elif name == 'vokswagen' or name == 'vw':
            return 'volkswagen'
        else:
            return name
        
    def _load_data(self):
        source_file = 'auto-mpg.clean.txt'
        data_file = "auto-mpg.data.txt"

        if not os.path.exists(data_file):
            Logger.debug('Original Data file does not exists')
            Logger.info('Original Data file does not exists')
            self._get_data()
        
        elif not os.path.exists(source_file):
            Logger.debug("'auto-mpg.clean.txt' Data file does not exists")
            Logger.info("'auto-mpg.clean.txt' Data file does not exists")
            self._clean_data()

        record = collect.namedtuple('record',
                            ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'year',
                             'origin', 'name'])

        with open(source_file, 'r') as f:
            lines = csv.reader(f, delimiter=' ', skipinitialspace=True)
            self.year_data = collect.defaultdict(list)
            self.make_data = collect.defaultdict(list)
            for line in lines:
                information = record(mpg=line[0], cylinders=line[1], displacement=line[2], horsepower=line[3],
                                     weight=line[4], acceleration=line[5], year=line[6], origin=line[7], name=line[8])
                header = information.name.split()
                autoMPG=(AutoMPG(self.get_correct_name(header[0]), " ".join(header[1:]), f"19{information.year}", information.mpg))
                self.year_data[autoMPG.year].append(float(information.mpg))
                self.make_data[autoMPG.make].append(float(information.mpg))
                self.result.append(autoMPG)
            return self.result

    def _get_data(self):
        data_file = "auto-mpg.data.txt"
        if not os.path.exists(data_file):
            response = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")
            open("auto-mpg.data.txt", "wb").write(response.content)

        Logger.debug('Data file downloaded and stored')
        Logger.info('Data file downloaded and stored')
        
        self._clean_data()
        
    def _clean_data(self):
        with open('auto-mpg.data.txt') as f,open('auto-mpg.clean.txt','w') as f2:
            for line in f:
                row=line.strip()
                realresults=row.expandtabs(2)
                f2.write(realresults+"\n")

        Logger.debug("'auto-mpg.clean.txt' Data file created by using original Data")
        Logger.info("'auto-mpg.clean.txt' Data file created by using original Data")



    def __iter__(self):
        return self
    
    def __next__(self):
        if self.iter== len(self.result):
            raise StopIteration
        AutoCategories = self.result[self.iter]
        self.iter += 1
        return AutoCategories
    
    def sort_by_default(self):
        Logger.debug('Data sorted by default i.e. By order of Make, Model, Year & MPG')
        Logger.info('Data sorted by default i.e. By order of Make, Model, Year & MPG')
        return sorted(self.result)
    
    def sort_by_year(self):
        Logger.debug('Data sorted by Year i.e. By order of Year, Make, Model & MPG')
        Logger.info('Data sorted by Year i.e. By order of Year, Make, Model & MPG')
        return sorted(self.result, key=attrgetter('year', 'make', 'model', 'mpg') ) 

   
    
    def sort_by_mpg(self):
        Logger.debug('Data sorted by MPG i.e. By order of MPG, Make, Model & Year')
        Logger.info('Data sorted by MPG i.e. By order of MPG, Make, Model & Year')
        return sorted(self.result, key=attrgetter('mpg', 'make', 'model', 'year') )
    
    def mpg_by_year(self):        
        Logger.debug('Average MPG for all cars by Year')
        Logger.info('Average MPG for all cars by Year')
        return {year: sum(mpg_list)/len(mpg_list) for year,mpg_list in self.year_data.items()}

    
    def mpg_by_make(self):
        Logger.debug('Average MPG for all cars by Make')
        Logger.info('Average MPG for all cars by Make')
        return {make: sum(mpg_list)/len(mpg_list) for make,mpg_list in self.make_data.items()}
        
    

                
if __name__ == '__main__':
    ### Logger
    Logger = logging.getLogger()
    Logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(message)s')

    file_handler = logging.FileHandler('autompg3.log')
    file_handler.setFormatter(formatter)
    Logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    Logger.addHandler(stream_handler)

    ### Command Line Parsing
    parser = argparse.ArgumentParser(description='Parse data from specified data file')
    parser.add_argument('command', help='command to execute: print, mpg_by_year, mpg_by_make')
    parser.add_argument('-s', '--sortby', metavar='<sort order>', type=str, help='sort by year, sort by mpg and sort by default')
    parser.add_argument('-o', '--ofile', metavar='<outfile>', type=str, help='output file', default='sys.stdout')
    parser.add_argument('-p', '--plot', dest='plot', action='store_true', help='specified graphical output can be produced using matplotlib')

    args = parser.parse_args()
    autoMPGData = AutoMPGData()
    # print(args)

    if(args.command=='print'):
        if(args.sortby):
            if(args.sortby=="year"):
                data = autoMPGData.sort_by_year()
            elif(args.sortby=="mpg"):
                data = autoMPGData.sort_by_mpg()
            else:
                data = autoMPGData.sort_by_default()
        else:
            data = autoMPGData.sort_by_default()

        if(args.ofile):
            with open(args.ofile, 'w', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(["make","model","year","mpg"])
                for i in data:
                    Logger.info(i)
                    csvwriter.writerow([i.make,i.model,i.year,i.mpg])

    elif(args.command=='mpg_by_year'):        
        data = autoMPGData.mpg_by_year()
        if(args.plot):   
            # Below is used in case when file name is not specified and only '-p' option used;
            # in this case, the graph will be plotted AND data will be displayed + added in default file also
            with open(args.ofile, 'w', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(["year","Average mpg"])    
                for key in sorted(data):                    
                    Logger.info([key, data[key]])
                    csvwriter.writerow ((key, data[key]))

            plot.plot(sorted(data.keys()), [int(data[key]) for key in sorted(data.keys())])            
            plot.xlabel('Year')
            plot.ylabel('MPG')
            plot.title('MPG by Year')
            plot.show()

        elif(args.ofile):            
            with open(args.ofile, 'w', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(["year","Average mpg"])    
                for key in sorted(data):
                    # print ("%s: %s" % (key, data[key]))
                    Logger.info([key, data[key]])
                    csvwriter.writerow ((key, data[key]))
                        
    else:
        data =  autoMPGData.mpg_by_make()        
        if(args.plot):        
            with open(args.ofile, 'w', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(["make","Average mpg"])                  
                for key in sorted(data):                    
                    Logger.info([key, data[key]])
                    csvwriter.writerow ((key, data[key]))
            plot.bar(sorted(data.keys()), [int(data[key]) for key in sorted(data.keys())])            
            plot.xticks(rotation='vertical')
            plot.subplots_adjust(left=None, bottom=0.25, right=None, top=None, wspace=None, hspace=None)
            plot.xlabel('Make')
            plot.ylabel('MPG')                     
            plot.title('MPG by Make')
            plot.show()

        elif(args.ofile):
            with open(args.ofile, 'w', newline="") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(["make","Average mpg"])                  
                for key in sorted(data):
                    # print ("%s: %s" % (key, data[key]))
                    Logger.info([key, data[key]])
                    csvwriter.writerow ((key, data[key]))





 