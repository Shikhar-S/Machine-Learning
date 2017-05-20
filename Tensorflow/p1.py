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
root='./notMNIST_small'
for d in os.listdir(root):
	dd=os.path.join(root,d)
	if(os.path.isdir(dd)):
		for x in os.listdir(dd):
			display(Image(filename=(os.path.join(dd,x))))