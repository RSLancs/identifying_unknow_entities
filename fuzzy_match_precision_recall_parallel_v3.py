## Python 37

from pprint import pprint
import pandas as pd
import nltk
from sklearn.metrics import precision_recall_fscore_support as pr
from sklearn.metrics import confusion_matrix
import sklearn
import concurrent.futures
from functools import partial
import time
import datetime


def bio_bigrams_and_bio_match_bool(in_text):
	"""
	This function takes a BIO tagged text and creates a bigram list of 
	word tokens with a boolean I/O if the bigram is a BI match
	"""
	word_list = [] 
	tag_list = []
	plant_names_in_set = []

	for line in in_text: # iterate over all lines
		if line: # check line is not empty
			word, tag = line.split() # split line into word, tag

			word_list.append(word) # appends word to list
			tag_list.append(tag) # appends tag to list
		else:
			word_list.append(' ')
			tag_list.append('O')

	# print(word_list[:100], tag_list[:100])
	# print(len(word_list))

	word_bigramz = [' '.join(bigram) for bigram in nltk.bigrams(word_list)]# forms word bigrams
	#print(word_bigramz[:10])

	tag_bigramz = [' '.join(bigram) for bigram in nltk.bigrams(tag_list)]# forms tag bigrams
	#print(tag_bigramz[:10])

	assert len(word_bigramz) == len(tag_bigramz)# check bigram word and tag lists are same length

	# forms a boolean list of the bigrams
	bigram_bool = []
	for tag_pair in tag_bigramz:
		if tag_pair == 'B I':
			bigram_bool.append(1)
		else:
			bigram_bool.append(0)

	#print(bigram_bool[:12])

	bigrams_with_bool = list(map(list, zip(word_bigramz, bigram_bool)))

	# collect plant names as bool == 1 
	for bigram, bool in bigrams_with_bool:
		if bool == 1:
			plant_names_in_set.append(bigram)

	plant_names_in_set_clean = [plant.strip().lower() for plant in plant_names_in_set]

	print(bigrams_with_bool[:100])

	return bigrams_with_bool, list(set(plant_names_in_set_clean))



##.......check no overlap between datasets...........

def check_no_overlap(train_val_plants, test_plants):
	"""
	This function checks there is no overlap between the combined train and val plant list
	and the test plant list
	"""
	for plant_name in train_val_plants:
		assert plant_name not in test_plants, f'{plant_name} overlaps with test dataset'



##.......... fuzzy matching..............................

def fuzz_precision_recall(plant_list_in, edit_dist, bigrams_with_bool_in):
	"""
	This function uses edit distance to incrementally compare a list of input bigrams (plant names) against a bigram list.  
	"""

	fuzz_p_r = list(bigrams_with_bool_in)
	#print(fuzz_p_r)

	for ed in range(edit_dist): # iterate over each edit distance 
		#print(ed)
			
		match = False
		for plant in plant_list_in:
			#print(plant)
			edit_distance = nltk.edit_distance(bigrams_with_bool_in[0].strip().lower(), plant, substitution_cost=1, transpositions=False)#check edit-distance
				
			if edit_distance <= ed: #if edit-distance size is less than or equal to selected edit distance
				#print(f'bigram_word: {bigrams_with_bool_in[0]} and {plant} with ed {edit_distance}')
				match = True
				break ## once condition has been met - break out of look

		if match == True:
			fuzz_p_r.append(1)
			
		else:	
			fuzz_p_r.append(0)				
	
	return fuzz_p_r
						 

##.................precision and recall...............

def precision_recall_scores(prec_rec_counts_in):
	"""
	This function calculates precision, recall and f scores
	"""

	prediction_scores = [] 
	
	gold = [i[1] for i in prec_rec_counts_in]
	#print(gold)

	predictions = [i[2:] for i in prec_rec_counts_in]
	#print(predictions)

	for i in range(len(predictions[0])):
	
		predicted = [ed[i] for ed in predictions] # collect all perditions or i edit distance 
		
		# manually calculate precision, recall and fscore
		tn, fp, fn, tp = confusion_matrix(gold, predicted).ravel()
		precision = (tp/(tp+fp))
		recall = (tp/(tp+fn))
		fscore = (2*precision*recall)/(precision+recall)
		prediction_scores.append([i, precision, recall, fscore, tn, fp, fn, tp])
		
		# ## use sklearn to calculate precisions, recall, fscore
		# bPrecis, bRecall, bFscore, bSupport = pr(gold, predicted, average='binary')	
		# prediction_scores.append([i, bPrecis, bRecall, bFscore])	

	mydf = pd.DataFrame(prediction_scores, columns=['edit_dist','precision','recall','fscore','TrueNeg', 'FalsePos', 'FalseNeg', 'TruePos'])

	return mydf


##..........run script in parallel................

if __name__ == '__main__':
	
	with open('./data/train.txt', 'r', encoding="utf8") as f:
		train = f.read().split('\n') # read in train chunks and split on newline
	#pprint(train[:50])

	with open('./data/val.txt', 'r', encoding="utf8") as f:
		val = f.read().split('\n') # read in validate chunks and split on newline
	#pprint(val[:50])

	with open('./data/test.txt', 'r', encoding="utf8") as f:
		test = f.read().split('\n') # read in test chunks and split on newline
	#pprint(test[:50])

	test_with_bools, test_plant_bigrams = bio_bigrams_and_bio_match_bool(test) # collect all TEST bigrams/BIO tags as Bool and unique plantnames
	#print(test_with_bools)

	_, train_plant_bigrams = bio_bigrams_and_bio_match_bool(train) # collect all unique plantnames from train chunks 
	print(train_plant_bigrams)

	_, val_plant_bigrams = bio_bigrams_and_bio_match_bool(val)  # collect all unique plantnames from validate chunks 
	#print(val_plant_bigrams)

	train_val_plant_bigram = list(sorted(set(train_plant_bigrams + val_plant_bigrams), key=len)) # join train and validate plant names and remove any duplicates
	#print(train_val_plant_bigram)
	
	check_no_overlap(train_val_plant_bigram, test_plant_bigrams)# check there is no overlap between sets

	print('len on train plants: ', len(train_plant_bigrams), ' Len of val plants: ', len(val_plant_bigrams), ' Len of test plants: ', len(test_plant_bigrams), ' Len of train_val: ', len(train_val_plant_bigram))
	
	# reduce input lists for testing
	# train_val_plant_bigram = train_val_plant_bigram[100:200]
	# test_with_bools = test_with_bools[:100]
	# print(test_with_bools)

	ed = len(max(train_val_plant_bigram, key=len))
	#print(ed)

	## run in parallel to speed up edit distance matching 
	with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor: # set number of cores

		func = partial(fuzz_precision_recall, train_val_plant_bigram, ed) # use partial function to pass MULTIPLE variables to concurrent  
		results = executor.map(func, test_with_bools)

	join_finds = [] # join all parallel finds
	
	for finds in list(results):
		join_finds.append(finds)

	ts = time.time() # get time stamp for when script was run
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed
	
	## save out raw edit distance boolean's 
	ed_bools = pd.DataFrame(join_finds)
	ed_bools.to_csv('./data/bool_fuzz_precision_recall_' + str(st) + '.csv', index=False, header=False)

	scores_df = precision_recall_scores(join_finds) # parallel precisions and recall scores for each edit distance
	#print(scores_df)

	scores_df.to_csv('./data/fuzz_precision_recall_fscore_' + str(st) + '.csv', index=False, header=True)
	
	assert len(join_finds) == len(test_with_bools), 'input word list is not the same as output word list' # check output len is same as input len
