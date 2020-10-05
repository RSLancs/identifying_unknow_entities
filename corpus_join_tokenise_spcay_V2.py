## python 36 version

import re
from pprint import pprint 
import glob
import spacy
from spacy.tokenizer import Tokenizer
import time
import datetime




def open_single_file_read(file): 
	"""
	read in text from file and preform basic processing - join words split over two lines,
	add whitespace after fullstops, remove excessive whitespace 
	"""
	with open(file, 'r', encoding='utf-8-sig', errors='ignore') as f:
		print(file)
		raw_data = f.read() # read and lower text
		word_join1 = re.sub(r'-\s+\n+(\w+ *)', r'\1\n', raw_data)# join words split over 2 lines
		word_join2 = re.sub(r'-\n+(\w+ *)', r'\1\n', word_join1)# join words split over 2 lines
		word_join3 = re.sub(r'\n\n\n+',r'\n\n', word_join2)# remove excessive new lines
		fullstop_standard = re.sub(r'\.(?![\s])',r'. ', word_join3) # add a \s after '.' to help tokenization
		print(len(fullstop_standard))

	return fullstop_standard
	#return 'UNIQUETEXTIDENT' + file[28:-4] +'\n\n' + fullstop_standard + '\n\n' #28 for linux path, 39 for win


def custom_tokenizer(nlp):
	"""
	compile custom tokeniser that does not split words on punctuation on infix
	"""
	prefix_re = re.compile(r'''^[^a-zA-Z]''')
	suffix_re = re.compile(r'''[^a-zA-Z]$''')
	##infix_re = re.compile(r'''[-~]''')
	simple_url_re = re.compile(r'''^https?://''')

	return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                ##infix_finditer=infix_re.finditer,
                                token_match=simple_url_re.match)


def tokenise_text(text_it):
	"""
	word tokenizer using custom SpaCy tokeniser. Preserves new line splits
	"""
	nlp = spacy.blank('en')
	
	nlp.tokenizer = custom_tokenizer(nlp) # compile custom tokeniser

	line_split_text = [line for line in text_it.split('\n') if line != ''] # split text first by line

	line_split_text = [re.sub(r'\s+', r' ', line) for line in line_split_text] # reduce whitesspace 
		
	line_split_text = [line.strip() for line in line_split_text] # strip whitespace from lines - beginning/end

	tokenized_text = [[i.text for i in nlp(line)] for line in line_split_text] # split line into tokens with spacy
		
	tokenized_text = [t for t in tokenized_text if t != ''] # remove any blank lines

	return tokenized_text


def write_out(out_path, out_data):
	"""
	writes file out. Preserves new line splits as empty line
	"""
	thefile1 = open('./data/' + out_path + str(st) +'.txt', 'w', encoding ='utf8')

	for line in out_data:
		
		for item in line:
			thefile1.write("%s\n" % item)

		thefile1.write("\n")



#############################################################
##...set corpus directory and generate list of contents.............


files_in_folder_list = glob.glob('./corpus/*.txt') # ACTUAL corpus collect files in directory

#files_in_folder_list = files_in_folder_list[:3] # reduce corpus size for testing
#print(files_in_folder_list)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')# format time stamp to when POWO was accessed

whole_corpus = ''.join([open_single_file_read(f) for f in files_in_folder_list]) # read and join whole corpus

processed_tokenised_text = tokenise_text(whole_corpus) # tokenise whole corpus
#pprint(processed_tokenised_text)

write_out('full_spacy_split_MLcorpus_', processed_tokenised_text) # write tokenised corpus out to file
