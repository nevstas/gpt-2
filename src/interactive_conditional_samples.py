#!/usr/bin/env python3

import fire
import json
import os
import numpy as np
import tensorflow as tf
import model, sample, encoder
import time
import glob
import csv

script_path = os.path.dirname(os.path.realpath(__file__))

def writeln(filename, str):
    global script_path
    with open(script_path + "//" + filename, 'w', encoding="utf-8") as the_file:
        the_file.write(str)

def interact_model(
    model_name='124M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=0,
    top_p=1,
    models_dir='models',
):
    """
    Interactively run the model
    :model_name=124M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
     :models_dir : path to parent folder containing model subfolders
     (i.e. contains the <model_name> folder)
    """
    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)

        if not os.path.exists(script_path + '//..//result'):
            os.makedirs(script_path + '//..//result')
        files = glob.glob('result/*')
        for f in files:
            os.remove(f)

        print(time.strftime("%d.%m.%Y %H:%M:%S") + " Start")
        generated = 0
        with open('keywords.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            flag_first = False
            for row in spamreader:
                if not flag_first:
                    flag_first = True
                    continue
                raw_text = row[0]
                context_tokens = enc.encode(raw_text)
                for _ in range(nsamples // batch_size):
                    out = sess.run(output, feed_dict={
                        context: [context_tokens for _ in range(batch_size)]
                    })[:, len(context_tokens):]
                    for i in range(batch_size):
                        generated += 1
                        text = enc.decode(out[i])
                        text = os.linesep.join([s for s in text.splitlines() if s])
                        param = "category:" + row[1]
                        if row[2]:
                            param = param + "|title:" + row[2]
                        text = "param=" + param + "\n" + text
                        writeln("..//result//result" + str(generated) + ".txt", text)
                        print(time.strftime("%d.%m.%Y %H:%M:%S") + " result" + str(generated) + ".txt Done")
                      
                

if __name__ == '__main__':
    fire.Fire(interact_model)

