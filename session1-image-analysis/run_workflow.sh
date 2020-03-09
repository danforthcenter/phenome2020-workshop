#!/bin/bash

mkdir -p output_images

plantcv-workflow.py \
--dir ./ath_tcv_images \
--workflow ath_tcv_workflow.py \
--outdir ./output_images \
--adaptor filename \
--type JPG \
--meta plantbarcode,treatment,id,timestamp \
--json plantcv_results.json \
--cpu 4 \
--writeimg \
--create
