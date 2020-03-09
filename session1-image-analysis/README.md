
# Session 1: Image Analysis using PlantCV

Image data included here are a subset of the images from https://doi.org/10.6084/m9.figshare.7599923.v1. Files were renamed for alphanumeric sorting purposes and were rotated as needed for consistency but are otherwise unaltered from the originals.

## Pre-workshop: Setup environment

Prior to the workshop we set up environments for each participant using Amazon Web Services EC2 compute instances. To replicate the environment for session 1:

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Install PlantCV:

```bash
conda env create --file environment.yml
```

## Part 1: Develop an image analysis workflow with PlantCV

Start Jupyter:

```bash
jupyter notebook
```

Open the PlantCV workflow notebook `ath_tcv_workflow.ipynb` provided here. Make sure the kernel selected is one containing PlantCV (e.g. `Python [conda env:plantcv]`). In the workshop we started with a mostly empty notebook and built the workflow from scratch, but the notebook is provided here already filled in. The input image can be changed to any other image in the `ath_tcv_images` folder.

## Part 2: Convert the Jupyter workflow into a Python script

On the command line, convert the notebook to a Python script:

```bash
jupyter nbconvert --to python ath_tcv_workflow.ipynb
```

Open the script `ath_tcv_workflow.py` in your favorite text editor. Some modifications are needed to convert this to a script we can run in parallel using PlantCV. A clean script is included here, but here is a summary of the necessary changes:

Remove `get_ipython().run_line_magic('matplotlib', 'inline')`.

Add `import argparse` to the other imports.

Remove `pcv.__version__`.

Replace this code:

```python
class options():
	def __init__(self):
	    self.debug = "plot"
	    self.result = "results.txt"
	    self.outdir = "./output_images"
	    self.writeimg = False
	    self.image = "ath_tcv_images/tcv/Col-0_wt_#3_17dpi.JPG"
```    

with this code (source: https://plantcv.readthedocs.io/en/stable/jupyter/):

```python
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with PlantCV.")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-r","--result", help="Result file.", required= True )
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-w","--writeimg", help="Write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.")
    args = parser.parse_args()
    return args
```

Immediately after the `options` function, add: `def main():`.

Indent all remaining code by one tab.

At the end of the script add this code:

```python
if __name__ == '__main__':
    main()
```

Optionally, remove extra comments/documentation (for clarity only).

## Part 3: Run the workflow in parallel

We used a built-in feature of PlantCV to run the workflow over the 80 images in the dataset. We provide a Bash script that runs `plantcv-workflow.py` on the Python workflow script made in Part 2. The meaning of the inputs is:

`--dir ./ath_tcv_images` - This is the input directory of images. It is okay that they are in subdirectories.

`--workflow ath_tcv_workflow.py` - This is the Python workflow script.

`--outdir ./output_images` - This is an output directory where output images will be saved.

`--adaptor filename` - The input images and metadata are in the "filename" format. I.e. all the metadata is in the filenames.

`--type JPG` - This is the file extension on the images.

`--meta plantbarcode,treatment,id,timestamp` - The metadata encoded in the images is plantbarcode (plant name, genotype, etc.), treatment, identifier, and timestamp (in this case just days post innoculation).

`--json plantcv_results.json` - This is the name of the output file.

`--cpu 8` - This is how many parallel processes we will use.

`--writeimg` - Sets the directive to save output images to True.

`--create` - Forces the program to overwrite the output file `plantcv_results.json` if it already exists.

To run the workflow analysis, on the command-line run:

```bash
conda activate plantcv
bash run_workflow.sh
```

## Part 4: Export the PlantCV output to a tabular format

After running the workflow in parallel the outputs are stored in a JSON file (`plantcv_results.json` in this case). To convert this file into two tabular (CSV) files for use in R, run the following on the command-line:

```bash
conda activate plantcv
plantcv-utils.py json2csv --json plantcv_results.json --csv ath-tcv
```

This will produce two tables. `ath-tcv-single-value-traits.csv` contains measurements that have single values (e.g. area, height, width, etc.). `ath-tcv-multi-value-traits.csv` contains measurements that have a vector of values (e.g. a histogram of hue values).

## Part 5: Analyze the distribution of hue values

In Zheng et al. (2019), the distribution of plant hue values was used as a metric for assessing viral infection. To reproduce part of this analysis, open the notebook `analyze_infection_by_hue.ipynb` using Jupyter. Make sure the notebook kernel is set to use R (e.g. `R [conda env:plantcv]`). The notebook reads in the two trait files generated above and merges the single-value traits with the hue frequencies data. The hue frequency distribution for each plant is normalized to the plant size (area) and the normalized values are averaged over the replicates for each sample. The data are plotted using ridge plots from the package `ggridges`. 

## References

If you use materials from this workshop, please cite:

Zheng X, Fahlgren N, Abbasi A, Berry JC, Carrington JC. 2019. Antiviral ARGONAUTEs against *Turnip Crinkle Virus* revealed by image-based trait analysis. *Plant Physiology* 180:1418–1435. DOI: [10.1104/pp.19.00121](https://doi.org/10.1104/pp.19.00121).

Carrington Lab, James; Zheng, Xingguo (2019): Raw data for Antirival ARGONAUTE protein during TCV infection revealed by Image-based trait analysis in Arabidopsis. figshare. Dataset. https://doi.org/10.6084/m9.figshare.7599923.v1.
