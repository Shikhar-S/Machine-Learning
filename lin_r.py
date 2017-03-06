from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
from six.moves import cPickle as pickle

data_root='.'
pickle_file = os.path.join(data_root, 'notMNIST.pickle')
numberSamples=200000
numberTest=10000
with open(pickle_file,'rb') as f:
	S=pickle.load(f)
	print(S['train_dataset'].shape,S['test_dataset'].shape)
	permutation=np.random.permutation(numberSamples)
	permutation_test=np.random.permutation(numberTest)
	train_X,train_Y = (S['train_dataset'][permutation],S['train_labels'][permutation])
	test_X,test_Y= (S['test_dataset'][permutation_test],S['test_labels'][permutation_test])
	train_x=np.ndarray(shape=(numberSamples,28*28),dtype=float)
	test_x=np.ndarray(shape=(numberTest,28*28),dtype=float)
	for i in range(0,numberSamples):
		train_x[i]=np.reshape(train_X[i],(28*28))
	for i in range(0,numberTest):
		test_x[i]=np.reshape(test_X[i],(28*28))
	Model=LogisticRegression()
	Model.fit(train_x,train_Y)
	print(Model.score(test_x,test_Y))