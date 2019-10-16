#!/bin/bash -l
#SBATCH --job-name=en_cs
#SBATCH --cpus-per-task=4
#SBATCH --mem=50gb
#SBATCH --time=23:55:00
#SBATCH --gres=gpu:0

#SBATCH --array=1-10

module load tensorflow/1.3.0-py36-gpu
module load python/3.6.13
#module load keras/1.1.0 
module load cuda cudnn/v8
module load opencv/2.4.13


(( n = SLURM_ARRAY_TASK_ID ))
(( end = n * 100))
(( start = end - 100))
python ./encoding_cont_sty.py $start $end