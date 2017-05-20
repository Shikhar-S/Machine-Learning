from __future__ import print_function
import numpy as np
import tensorflow as tf
from six.moves import cPickle as pickle
from six.moves import range

pickle_file = 'notMNIST.pickle'

with open(pickle_file, 'rb') as f:
  save = pickle.load(f)
  train_dataset = save['train_dataset']
  train_labels = save['train_labels']
  valid_dataset = save['valid_dataset']
  valid_labels = save['valid_labels']
  test_dataset = save['test_dataset']
  test_labels = save['test_labels']
  print('Training set', train_dataset.shape, train_labels.shape)
  print('Validation set', valid_dataset.shape, valid_labels.shape)
  print('Test set', test_dataset.shape, test_labels.shape)

print("###############REFORMATTING################")
image_size = 28
num_labels = 10

def reformat(dataset, labels):
  dataset = dataset.reshape((-1, image_size * image_size)).astype(np.float32)
  labels = (np.arange(num_labels) == labels[:,None]).astype(np.float32)
  return dataset, labels

train_dataset, train_labels = reformat(train_dataset, train_labels)
valid_dataset, valid_labels = reformat(valid_dataset, valid_labels)
test_dataset, test_labels = reformat(test_dataset, test_labels)
print('Training set', train_dataset.shape, train_labels.shape)
print('Validation set', valid_dataset.shape, valid_labels.shape)
print('Test set', test_dataset.shape, test_labels.shape)

def accuracy(predictions, labels):
  return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
          / predictions.shape[0])


###########################MODEL######################
def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

batch_size=256
graph=tf.Graph()

with graph.as_default():
  tf_train_dataset= tf.placeholder(tf.float32,shape=[batch_size,image_size*image_size])
  tf_train_labels= tf.placeholder(tf.float32,shape=[batch_size,num_labels])
  tf_valid_dataset=tf.constant(valid_dataset)
  tf_test_dataset=tf.constant(test_dataset)
  keep_probability=tf.placeholder(tf.float32)
  W1=weight_variable([image_size*image_size,1024])
  W2=weight_variable([1024,num_labels])
  B1=bias_variable([1024])
  B2=bias_variable([num_labels])
  hyperparam_W1=tf.constant(0.1,)
  hyperparam_W2=tf.constant(0.1)
  hidden_output=tf.nn.dropout(tf.nn.relu(tf.matmul(tf_train_dataset,W1)+B1),keep_probability)
  logits=tf.matmul(hidden_output,W2)+B2
  Objective=tf.reduce_mean(tf.add(tf.nn.softmax_cross_entropy_with_logits(labels=tf_train_labels,logits=logits),0.000*(tf.nn.l2_loss(W1)+tf.nn.l2_loss(W2)))) #turning off L2 regularization
  optimizer=tf.train.GradientDescentOptimizer(0.5).minimize(Objective)
  train_prediction=tf.nn.relu(logits)
  test_prediction=tf.nn.relu(tf.matmul(tf.nn.dropout(tf.nn.relu(tf.matmul(tf_test_dataset,W1)+B1),keep_probability),W2)+B2)
#########################SESSION#########################

num_steps = 3001 #gives 94.2% accuracy at 3000

with tf.Session(graph=graph) as session:
  tf.global_variables_initializer().run()
  print("Initialized")
  for step in range(num_steps):
    offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
    # Generate a minibatch.
    batch_data = train_dataset[offset:(offset + batch_size), :]
    batch_labels = train_labels[offset:(offset + batch_size), :]
    feed_dict = {tf_train_dataset : batch_data, tf_train_labels : batch_labels, keep_probability: 0.5}
    _, l, predictions = session.run([optimizer, Objective, train_prediction], feed_dict=feed_dict)
    if (step % 500 == 0):
      print("Minibatch loss at step %d: %f" % (step, l))
      print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
  feed_dict[keep_probability]= 1.0;
  print("Test accuracy: %.1f%%" % accuracy(test_prediction.eval(feed_dict), test_labels))


