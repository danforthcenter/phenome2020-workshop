# Session 2: Deep Learning using Deep Plant Phenomics

## Pre-workshop: Setup environment

Prior to the workshop we set up environments for each participant using Amazon Web Services EC2 p3.2xlarge compute instances with NVIDIA V100 GPU compute modules. 

To replicate the software environment for session 2:

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Install Deep Plant Phenomics:

```bash
conda env create --file environment.yml
```

Alternatively, follow the instructions at https://github.com/p2irc/deepplantphenomics.

## Download training data

Aerial images of sorghum with panicles and labels are available from Guo et al. (2018). The data is available upon request from the authors by submitting a form at https://docs.google.com/forms/d/e/1FAIpQLSeAtefEzXEQW1Yo7rSZth3Yjzoc9SJfNDQQFKYXDwEPlWSV1w/viewform?c=0&w=1.

The data should be downloaded into a folder in this directory called `dataset1`.

## Training the sorghum panicle counter model

Start Jupyter:

```bash
jupyter notebook
```

The Jupyter notebook `dpp.ipynb` contains the code for training the Deep Plant Phenomics [HeatmapObjectCountingModel](https://deep-plant-phenomics.readthedocs.io/en/latest/Tutorial-Object-Counting-with-Heatmaps/). The notebook will read the training data from the `dataset1` folder and will save results to a folder called `tensorlogs`.

Training performance can be monitored using Tensorboard. To start Tensorboard run:

```bash
tensorboard --logdir tensorlogs
```

Note: training on a machine with an NVIDIA V100 GPU module (or equivalent) takes less than 10 minutes. Training with an NVIDIA Tesla K80 GPU module (or equivalent) takes about 45 minutes. Training on a machine without a GPU module (CPUs only) will take significantly longer.

## Deploy the trained panicle counter model

Use the Jupyter notebook `deployment_test` as an example of how to deploy the trained model in an application.

## References

Guo W, Zheng B, Potgieter AB, Diot J, Watanabe K, Noshita K, Jordan DR, Wang X, Watson J, Ninomiya S, Chapman SC. 2018. Aerial Imagery Analysis - Quantifying Appearance and Number of Sorghum Heads for Applications in Breeding and Agronomy. *Frontiers in Plant Science* 9:1544. DOI: [10.3389/fpls.2018.01544](https://doi.org/10.3389/fpls.2018.01544).