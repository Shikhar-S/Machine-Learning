import json
import tensorflow as tf
import utils
import math
import numpy as np

tweet_sz=20 #Max tweet size
hidden_units=100 # 100 LSTM cells in one layer
vocab_size = 7597 # size of language
batch_size = 64 # for SGD on batches of size 64

#this function defines a linear layer based on input and output size given as arguments. Needed for final layer of model.
def linear(input_,output_sz,name,init_bias=0.0):
    shape = input_.get_shape().as_list()
    with tf.variable_scope(name):
        W = tf.get_variable("weight_matrix", [shape[-1], output_sz], tf.float32, tf.random_normal_initializer(stddev=1.0 / math.sqrt(shape[-1])))
    if init_bias is None:
        return tf.matmul(input_, W)
    with tf.variable_scope(name):
        b = tf.get_variable("bias", [output_sz], initializer=tf.constant_initializer(init_bias))
    return tf.matmul(input_, W) + b






# making placeholders for tweets and labels

tweets = tf.placeholder(tf.float32,shape=[None,tweet_sz,vocab_size]) 
# One hot representation of tweets. First Arg is None to allow for variable batch size.
labels = tf.placeholder(tf.float32,shape=[None])
# Single label for each tweet. Whether + or -.

LSTM_first = tf.contrib.rnn.BasicLSTMCell(hidden_units) # makes a layer of 100 LSTM cells
LSTM_second= tf.contrib.rnn.BasicLSTMCell(hidden_units) # variants are possible-> https://www.tensorflow.org/api_guides/python/contrib.rnn#Core_RNN_Cells_for_use_with_TensorFlow_s_core_RNN_methods
wrapped_LSTM= tf.contrib.rnn.MultiRNNCell(cells=[LSTM_first,LSTM_second],state_is_tuple=True)
#Wrap both lstm layers together into one single Multi RNN cell *why*

#To define a way to unroll the layers in time (dynamically/statically) and combine with inputs.
output, last_states = tf.nn.dynamic_rnn(
	cell = wrapped_LSTM,
	inputs = tweets,
	dtype = tf.float32)

sentiment = linear(last_states[-1][-1],1,name='output') #define last layer to be a linear combination of last state 
#input_ is state after last tweet's last word
sentiment=tf.squeeze(sentiment,[1]) # dont know why? squeeze is used to reshape tensor.



prob = tf.nn.sigmoid(sentiment) #apply sigmoid on the logit
prediction = tf.to_float(tf.greater_equal(prob, 0.5)) #if probability > 0.5 then prediction= positive else neg
pred_err = tf.to_float(tf.not_equal(prediction, labels)) #returns 1 if prediction does not match label
pred_err = tf.reduce_sum(pred_err) # sum prediction errors for individual tweets of batch




#defining Loss now as in usual deep net/ neural net
loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=sentiment,labels=labels)
loss = tf.reduce_mean(loss)

#define optimizer
optimizer=tf.train.AdamOptimizer().minimize(loss)

with tf.Session() as Sess:
    tf.global_variables_initializer().run(session=Sess)

    #make data ready for training and testing 
    train_data = json.load(open('data/trainTweets_preprocessed.json', 'r'))
    train_data = list(map(lambda row:(np.array(row[0],dtype=np.int32),str(row[1])),train_data))

    train_tweets = np.array([t[0] for t in train_data])
    train_labels = np.array([int(t[1]) for t in train_data])

    test_data = json.load(open('data/testTweets_preprocessed.json', 'r'))
    test_data = map(lambda row:(np.array(row[0],dtype=np.int32),str(row[1])),test_data)

    test_data = test_data[0:1000] 
    test_tweets = np.array([t[0] for t in test_data])
    test_labels = np.array([int(t[1]) for t in test_data])

    one_hot_test_tweets = utils.one_hot(test_tweets, vocab_size)
    


    #########training#######
    num_steps=1000

    for step in xrange(num_steps):
        
        offset=step*batch_size % (len(train_data)-batch_size)

        batch_tweets=utils.one_hot(train_tweets[offset:offset+batch_size],vocab_size) #converts this batch to one hot encoding
        batch_labels=train_labels[offset:offset+batch_size]

        data={tweets:batch_tweets,labels:batch_labels} #feed dictionary for run function

        T=Sess.run([optimizer,loss,pred_err],feed_dict=data)

        
        if(step%50==0):
            #testing
            test_loss=[]
            test_err=[]
            for batch_num in range(int(len(test_data)/batch_size)):
                test_offset = (batch_num * batch_size) % (len(test_data) - batch_size)
                test_batch_tweets = one_hot_test_tweets[test_offset : (test_offset + batch_size)]
                test_batch_labels = test_labels[test_offset : (test_offset + batch_size)]
                data_testing = {tweets: test_batch_tweets, labels: test_batch_labels}
                F= Sess.run([loss,pred_err], feed_dict=data_testing)
                test_loss.append(F[0])
                test_err.append(F[1])

            print 'Step number---> ', step
            print 'Train and test errors --> ',
            print T[2],
            print np.mean(test_err)
              # print step, test_loss, loss






