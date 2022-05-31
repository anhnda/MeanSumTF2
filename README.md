# Update code of MEANSUM to new package versions


## General setup 

Install conda environment
```
conda env create -f env.yml
conda activate m2
```


Execute inside ```scripts/```:

##### Create directories that aren't part of the Git repo (checkpoints/, outputs/):

```
bash setup_dirs.sh
```



##### The default parameters for Tensorboard(x?) cause texts from writer.add_text() to not show up. Update by:

```
python update_tensorboard.py
```



## Downloading data and pretrained models

### Data

1. Download Yelp data: https://www.yelp.com/dataset and place files in ```datasets/yelp_dataset/```
2. Run script to pre-process script and create train, val, test splits:
    ```
    bash scripts/preprocess_data.sh
    ```
3. Run script to generate subwordencoder:
   ```
   
   PYTHONPATH=. python data_loaders/build_subword_encoder.py --dataset=gene --tp=0 --output_dir=./ --output_fn=subwordenc
   ```

   ```
   cp subwordenc.pkl datasets/yelp_dataset/processed/
   ```
   Re-run train-test splitting...

4. Train language model:
   ```
   python pretrain_lm.py
   ```
   Copy the one trained model (.pt file) from checkpoints/lm/mlstm/yelp  to: stable_checkpoints/lm/mlstm/yelp


### Reference summaries

Download from: [link](https://s3.us-east-2.amazonaws.com/unsup-sum/summaries_0-200_cleaned.csv).
Each row contains "Input.business_id", "Input.original_review_\<num\>\_id", 
"Input.original_review__\<num\>\_", "Answer.summary", etc. The "Answer.summary" is the
reference summary written by the Mechanical Turk worker.


## Running

Testing with pretrained mode. This will output and save the automated metrics. 
Results will be in ```outputs/eval/yelp/n_docs_8/unsup_<run_name>```

NOTE: Unlike some conventions, 'gpus' option here represents the GPU ID (the one which is visible) and NOT the number of GPUs. Hence, for a machine with a single GPU, you will give gpus=0
```
python train_sum.py --mode=test --gpus=0 --batch_size=16 --notes=<run_name>
```

Training summarization model (using pre-trained language model and default hyperparams).
The automated metrics results will be in ```checkpoints/sum/mlstm/yelp/<hparams>_<additional_notes>```.:
```
python train_sum.py --batch_size=16 --gpus=0,1 --notes=<additional_notes> 
```
