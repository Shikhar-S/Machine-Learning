from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
data_root='.'
pickle_file = os.path.join(data_root, 'notMNIST.pickle')
test_to_valid=0

with open(pickle_file,'rb') as f:
	S=pickle.load(f)
	print(S['train_dataset'].shape)
	print(S['test_dataset'].shape)
	print(S['valid_dataset'].shape)
	t=0
	for y in S['test_dataset']:
		for z in S['valid_dataset']:
			if(y==z).all():
				test_to_valid+=1
				break
		t+=1
	print(test_to_valid/10000.0," % overlap between test and valid datasets")