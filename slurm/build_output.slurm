#!/bin/sh
# SLURM directives
#
#SBATCH --job-name=build_output
#SBATCH --array=[0-961]
#SBATCH --ntasks=1
#SBATCH --mem 1000
#SBATCH --oversubscribe
#SBATCH --ntasks-per-node=6

cd /scratch/kevin/imagine/`printf %06d ${SLURM_ARRAY_TASK_ID}`
tar -cvzf `printf %06d ${SLURM_ARRAY_TASK_ID}`.tar.gz *.ms *.csv
