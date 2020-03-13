# Session 3: Hyperspectral Image Analysis

The hyperspectral image analysis secion covered four topics:

1. Introduction to hyperspectral images and analysis.
2. Hyperspectral unmixing: decomposing a hyperspectral image into the pure spectral sigatures found in the scene.
3. Hyperspectral target detection: determining whether a particular target signature is found in each pixel of an image.
4. Hyperspectral classification: classify each pixel into one of a set of groups.

The workshop materials are hosted by the GatorSense team on [GitHub](https://github.com/GatorSense/HyperspectralAnalysisIntroduction) but are also linked in this repository.

## Pre-workshop: Setup environment

Prior to the workshop we set up environments for each participant using Amazon Web Services EC2 compute instances. To replicate the environment for session 3:

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Install dependencies:

```bash
conda env create --file environment.yml
```

Alternatively, follow the instructions at https://github.com/GatorSense/HyperspectralAnalysisIntroduction.

Start Jupyter:

```bash
jupyter notebook
```

Then open each of the notebooks to work through the exercises.
