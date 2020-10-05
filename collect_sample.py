##Python37

import random
from pprint import pprint
import pandas as pd
import re
import time
import datetime


# read in bio chunk txt file
with open('./data/bio_tagged_corpus_feb_2020-03-01.txt', 'r', encoding='utf8') as f:
	bio_chunks = f.read().split('\n\n') # read and split on empty lines

pprint(len(bio_chunks))


def get_bio_chunks(input_text):
	'''
	Collects only chunk that contain 'B', 'I' tags
	'''
	bio_chunk = []
	for chunk in input_text:	
		split_chunk = chunk.split('\n')

		tags = [i.split()[1] for i in split_chunk if i != '']
	
		if 'B' in tags:
			bio_chunk.append(chunk)
	return bio_chunk

tagged_chunks = get_bio_chunks(bio_chunks)


#....set sample..............
sample_size = 100 # set sample size

# collect sample
sorted_sample = [tagged_chunks[i] for i in sorted(random.sample(range(len(tagged_chunks)), sample_size))]
#print(sorted_sample)

#.......... write to csv.........

## get time script was run
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed


process_sample = [re.sub(r'\n', r' ', s) for s in sorted_sample] # replace new lines for space
mydf = pd.DataFrame(process_sample) # transform list to dataframe
mydf.to_csv('./data/100_SAMPLE_tagged_BIO_out_' + str(st) + '.csv', index=False, header=True)# write results out to file


#.......sort sample into correct BIO format and write to txt.................

space_sample = []
for chunk in sorted_sample:
	pro_sample = chunk.split('\n')
	for word in pro_sample:
		space_sample.append(word)
	space_sample.append('')
	
thefile = open('./data/100_SAMPLE_tagged_BIO_out_' + str(st) + '.txt', 'w', encoding='utf8')

for item in space_sample:
	 	thefile.write("%s\n" % item)
