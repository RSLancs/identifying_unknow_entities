## python 37

import pandas as pd

## Read in ML finds
ml_finds_df = pd.read_csv('./data/unknown_plant_names.tsv', '\t')
print(ml_finds_df.head())


def count_floor(in_df, count):
	"""
	Get finds found more than x times
	"""
	floor_df = in_df.groupby('bigram').filter(lambda x: len(x) >= count)
	print(floor_df.head())

	return floor_df



def means(in_df):
	"""
	Get mean of conf colum
	"""
	mean_df = in_df.groupby('bigram')['conf'].mean().sort_values(ascending=False)
	print(mean_df.head())

	return mean_df



floor_ml = count_floor(ml_finds_df, 1) # filter results by min find number

mean_floor_ml = means(floor_ml) # get mean conf of finds
print(len(ml_finds_df), len(floor_ml))


mean_floor_ml.to_csv('./data/MEAN_unknown_plant_names.csv') # write out results to csv


