## Python 37

from pprint import pprint
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import sklearn


bools = pd.read_csv('./data/bool_fuzz_precision_recall_2020-03-14.csv')
bools_list = bools.values.tolist()
#print(bools_list)

def precision_recall_scores(prec_rec_counts_in):
	""" 
	This function uses the raw output of fuzzy_match_precision_recall_parallel_v3.py 
	to caculate precision, recall and fscore from edit distance matching.
	"""

	prediction_scores = [] 
	
	gold = [i[1] for i in prec_rec_counts_in]
	#print(gold)

	predictions = [i[2:] for i in prec_rec_counts_in]
	#print(predictions)

	for i in range(len(predictions[0])):
	
		predicted = [ed[i] for ed in predictions]
		# if i == 5:
		# 	print(predicted)

		tn, fp, fn, tp = confusion_matrix(gold, predicted).ravel()

		precision = (tp/(tp+fp))

		recall = (tp/(tp+fn))

		fscore = (2*precision*recall)/(precision+recall)

		prediction_scores.append([i, precision, recall, fscore])

	mydf = pd.DataFrame(prediction_scores, columns=['edit_dist','precision','recall','fscore'])

	return mydf

prf = precision_recall_scores(bools_list)
# print(prf)

ax1 = prf.plot(x='edit_dist', y='precision', label="precision")
ax2 = prf.plot(x='edit_dist', y='recall', color='black', ax=ax1, label="recall")
ax2 = prf.plot(x='edit_dist', y='fscore', color='red', ax=ax1, label="fscore")

plt.legend(loc="upper left")
plt.ylim(0, 1.3)
plt.xlabel('Edit Distance')
plt.ylabel('Score')
#plt.axis([0, 20, -1, 1.5])

plt.savefig('./data/fuzz_precision_recall_fscore_line.png') # save plot
plt.show() # show plot