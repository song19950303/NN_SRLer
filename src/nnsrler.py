# -*- coding: utf-8 -*-
from __future__ import division, print_function
from data_utils import *
from config import configure
from model import *
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

    # read in dictionaries
    dicts = load_dictionaries(configure) # word2idx, idx2word, postag2idx, idx2postag, label2idx, idx2label

    # initialize LSTM SRL model
    model = LSTMSRLer(configure, idx2label=dicts[-1], label2idx=dicts[-2])

    # do training
    if configure['do_train']:
        # build computation graph for training
        model.compile(training=True)
        logging.info("Finished building computation graph for training.")

        # load data
        train_data = train_data_loader(dicts, configure, configure["training_data_path"])
        val_data = train_data_loader(dicts, configure, configure["validate_data_path"])
        logging.info("Read in training data successfully.")

        # run training process
        model.train(*(train_data+val_data), save_per_epoch=True)
        logging.info("Training process has been finished.")

    if configure['do_predict']:
        # build computation graph for prediction
        model.compile(training=False)
        logging.info("Finished building computation graph for testing.")

        # load data
        raw_test_data, test_feats = test_data_loader(dicts, configure)
        logging.info("Read in testing data successfully.")

        # load model and run testing process
        preds = model.test(raw_test_data, test_feats)
        logging.info("All of test sentences have been labelled.")

        # write output file
        write_outputs(preds, configure, idx2label=dicts[5])
        logging.info("Prediction output has been saved to %s" % configure['output_path'])