# Comparing Precision, Recall and fscore when using Edit Distance vs Machine Learning to match 'unknown' plant names in Scientific Journals 


## Overview 

The scripts in this repository form half of a project that examines the ability of rule based (edit distance) and Machine Learning approaches to identify 'unknown' entities from an input search list. They allow for a plant name search list, which includes historical synonyms, to be searched across a corpus of scientific text. All exact matches are extracted along with a chunk of co-text. These are then split into training, validate and test datasets whereby there is NO overlap in the plant names across the three datasets. The plant names from the train and validate datasets are used to search the test dataset and the precision, recall and fscore is calculated at different edit distances. The results are then plotted.   


## Requirements and Installation
1. Install Python 3.7
2. `pip install -r requirements.txt`
3. Download the scripts and the [./data/](./data/) and [./corpus/](./corpus/) folders.


## Getting Plant Name Synonyms  

Running the script [POWO_lookup_2020.py](./POWO_lookup_2020.py) uses Plants of the World Online (POWO) http://www.plantsoftheworldonline.org/ to look up plant name synonyms from an input list of modern plant names. It outputs a .csv files where the column contains all input plant names and all subsequent columns any found synonyms. 


## Cleaning and Joining Corpus of Scientific Texts

The script [corpus_join_tokenise_spcay_V2.py](./corpus_join_tokenise_spcay_V2.py) takes a corpus of .txt scientific texts, clean, tokenises and merges them into a single .txt file. All word token are saved on a new line. New lines are saves as an empty line. For example, the sentence:

The weather cleared as we advanced, and we had an extensive view
of rugged and broken mountains; not, according to Gilpin's distinction,
a mountain view

When cleaned, tokenised and split onto new linews, becomes:

The
weather
cleared
as
we
advanced
,
and
we
had
an
extensive
view

of
rugged
and
broken
mountains
;
not
,
according
to
Gilpin's
distinction,

a
mountain
view



## BIO Tagging Scientific Texts using Plant List

The script [bio_tag_corpus.py](./bio_tag_corpus.py) searches the merged scientific corpus using the plant list with synonyms. All exact matches are tagged as B (beginning) and I (inside), with all other tokens are tagged as O (outside). For example:

Agapanthus B
umbellatus I
African O
Blue O
Lily O
. O

To improve performance a dictionary of all unique bigrams is first generated, with the brigrams as keys and the bigrams index across the text as a list. When searching a large corpus of texts witt a very large plant name search list this methods greatly improves performance.

All texts chunks that contain a plant name match are then extracted as a .txt file.


## Splitting The Tagged Corpus

The corpus is then split into train, test, validate, ensuring that no plant names appear across the splits 

[information of scripts to be added]


## Measuring Precision, Recall, Fscore when using Edit Distance to match plant names across the splits

The script [fuzzy_match_precision_recall_parallel_v3.py](./fuzzy_match_precision_recall_parallel_v3.py) collects all of the plant names contained within the train, validate and test splits. The train and validate plant names are combined. This list of plant names is then compared against all bigrams in the test dataset and the edit distance is calculated. At each edit distance step between 0 to 30 (the max edit distance corresponds to the longest plant name in the input plant list) a 0 or 1 boolean value is for each bigram in the test dataset. The results are written out as a .csv where the first column is the bigram, the second column is the true BIO tag and the subsequent columns are the edit distances. For example:    


plant name|BIO tag|ed0|ed1|ed2|ed3|ed4|ed5|ed6|ed7|ed8|ed9|ed10
:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:
Potamogeton serratus|1|0|0|0|0|1|1|1|1|1|1|1
five of|0|0|0|0|0|0|0|1|1|1|1|1

(*Note - there is an efficiency glitch in this script whereby the edit-distance is recalculated for each edit distance step. This was done for simplicity, but could be sped up a lot)

## Geoparsing the collocates 

The script [plot_fuzzy_prf.py](./plot_fuzzy_prf.py) uses the boolean output form the script above to calculate the precision, recall and fscore at each edit-distance, in this case 0 to 30. The results are then saved as a .csv and plotted.    


## Additional scripts 

The script [collect_sample.py](./collect_sample.py) collects a sample of chunks containing BI tags from the whole tagged corpus.  

The script [filter_ml_results.py](./filter_ml_results.py) groups all unique bigrams in the corpus and calculates the mean ML conf score.  






