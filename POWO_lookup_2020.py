import re
import pandas as pd
import numpy as np 
import csv
import pickle
import os 
import json
import pykew.powo as powo
from pykew.powo_terms import Name
from pprint import pprint
import datetime
import time


##...........get time stamp for api POWO lookup query.....................

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed


###................. kingdom query.............. 

print('lookup started')
query = { Name.kingdom: 'Plantae' } # compile query
results = powo.search(query) # use query to search POWO


##....sort though POWO look up results

download_species = []	
for i in results: # iterate over results
		
	if 'name' in i: # if 'name' field in results
		if i['rank'] == 'Species': # if rank == 'species'
			#print(i)
			download_species.append(i['name'])

			
print(len(download_species))
print(len(list(set(download_species))))

##... get only binomial plant names

binome_spc = []
for i in list(set(download_species)):
	a = i.split()
	
	if len(a) != 2:
		print(a)
	else:
		binome_spc.append(i)

print(f'Full POWO plant list: {len(binome_spc)}. Uniuqe POWO plant list: {len(list(set(binome_spc)))}')


##........write out unique plane list.............

thefile = open('./data/POWO_binomial_unique_plant_list_' + str(st) + '.txt', 'w')

for item in binome_spc:
 	thefile.write("%s\n" % item)
