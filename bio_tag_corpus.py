## python 37

from pprint import pprint
import pandas as pd
import nltk
import csv
import time
import datetime
import json

def clean_plant_list(plant_list_in):
	"""
	Removes abbreviation plant names and duplicate plant names from input plant list if present
	"""
	full_plants = [plant for plant in plants if '.' not in plant] #remove abbreviation
	#print(full_plants)

	return list(set(full_plants)) # return unique names as list
	

def create_mapped_bigrams(in_text):
	"""
	Takes a split text and creates a bigram dictionary with words as keys and the words index across the text as a list 
	"""
	word_list = [] 

	for word in in_text: # iterate over words in corpus
		word_list.append(word.lower().strip()) # strip and lower all words in corpus
			
	word_bigramz = [' '.join(bigram) for bigram in nltk.bigrams(word_list)] # form bigrams
	print(f'Total word bigrams in corpus: {len(word_bigramz)}')

	# create unique bigram dict of corpus
	bigram_dict = {}

	for i, bigram in enumerate(word_bigramz):

		if not bigram in bigram_dict:# if bigram not already a dict key
			bigram_dict[bigram] = [] # make it a dict key

		bigram_dict[bigram].append(i) # add indices to dict key as value


	print(f'Unique bigrams in corpus: {len(bigram_dict)}')
	return bigram_dict


def get_plant_name_indices_matches(bigram_dict_in, plant_name_in):
	"""
	collect all plant name match instance indices
	"""
	finds = []
	for plant in plant_name_in: # iterate over all plant names in list
	
		plant = plant.lower().strip() # strip and lower each plant name
	
		find = bigram_dict_in.get(plant) # check plant name matches any bigram in corpus dict
	
		if find:# if plabt name matches any bigram in corpus dict
			finds.append([plant, find]) # append plant name and all corpus indices to list

	return finds


def create_match_instance_pairs(plant_match_in):
	"""
	sort match index instances removing ambiguous matches and creating match 'B', 'I' dict

	"""
	## collect all plant name match instances indices
	just_indices = [int(indices) for plant_match_in_set in plant_match_in for indices in plant_match_in_set[1]]
	
	assert len(just_indices) == len(set(just_indices)) # check there are no exact duplicates in indices

	sorted_index = list(sorted(just_indices)) # sort indices small-large
	print(f'Length of corpus bigrams BEFORE ambiguous matches removed: {len(sorted_index)}')
	#print(sorted_index)

	# remove all ambiguous matches that are within 1 word of each other
	print('Ambiguous plant name matches: ')
	for i, index in enumerate(sorted_index): # iterate over all indices in sorted list
		
		if index == sorted_index[i-1]+1: # indices is within 1 of previous indices in list
			print(index, sorted_index[i-1])
			sorted_index.remove(index) # remove indices from list
			sorted_index.remove(sorted_index[i-1]) # AND remove previous indices from list
	print(f'Length of corpus bigrams AFTER ambiguous matches removed: {len(sorted_index)}')

	# create indices dict with 'B', 'I' values
	paired_finds = {}
	for match_index in sorted_index: # iterate over unambiguous match indices list
					
			paired_finds[match_index] = ('B') # WITH value of 'B'
			
			paired_finds[match_index+1] = ('I') # WITH value of 'I'

	return paired_finds


def form_bios(paired_plant_match_in, text_in):
	"""
	tag corpus using match dict
	"""
	tagged_corpus =[]

	# used sorted and filtered indices to bio tag corpus
	for i, word in enumerate(text_in): # iterate over words in corpus
		if word: # if not white space
			find = paired_plant_match_in.get(i) # check if word index is in plant match dict keys
			#print(find)
			if find: # if match
				tagged_corpus.append(word + ' ' + str(find)) # append word to list WITH plant match dict value tag 
			else:
				tagged_corpus.append(word + ' O') # else append word to list with 'O' tag

		else:
			tagged_corpus.append(word)

	return tagged_corpus


def write_out(out_path, out_data):
	thefile = open(out_path, 'w', encoding='utf8')

	for item in out_data:
	 		thefile.write("%s\n" % item)


##.....................................................

## open full tokenised corpus
with open('./data/full_spacy_split_MLcorpus_2020-02-28.txt', 'r', encoding='utf-8', errors='ignore') as f:
	text = f.read().split('\n') # read in train chunks and split on newline
	#pprint(text[:50])

## open full plant list
with open('./data/POWO_binomial_unique_plant_list_2020-02-20.txt', 'r', encoding='utf-8', errors='ignore') as f:
	plants = f.read().split('\n') # read in train chunks and split on newline


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed

clean_plant_list = clean_plant_list(plants) # clean plant list
print(f'Plant list contains: {len(clean_plant_list)} unique plant names')

corpus_bigram_dict = create_mapped_bigrams(text) # transform corpus in to bigram dict

plant_name_matches = get_plant_name_indices_matches(corpus_bigram_dict, clean_plant_list) # get plant name matches with indices

plant_index_dict = create_match_instance_pairs(plant_name_matches) # get plant indices 'B', 'I' dict

bigram_bios = form_bios(plant_index_dict, text) # bio tag text


##..............................................

# write out csv plant name match indices 
results = pd.DataFrame(plant_name_matches)
results.to_csv('./data/plant_matches_index_' + str(st) + '.csv', index=True, header=False)

## write out json of corpus bigram dict
with open('./data/corpus_bigram_index_dic_' + str(st) + '.json', 'w') as fp:
	json.dump(corpus_bigram_dict, fp)

## write out bio text
write_out('./data/bio_tagged_corpus_feb_' + str(st) + '.txt', bigram_bios)
