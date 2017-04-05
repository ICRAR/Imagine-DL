#!/bin/bash --login
# SLURM directives
#
#SBATCH --job-name=produce-csv
#SBATCH --array=0-30
#SBATCH --ntasks=5
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5

cd /scratch/kevin/imagine/`printf %06d ${SLURM_ARRAY_TASK_ID}`
/usr/local/bin/casa --nologger --log2term -c /home/kevin/Imagine-DL/casa_scripts/create_raw_csv_file.py
