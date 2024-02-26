# LAI-NET
Make sure to install requirements listed in ./LAI-Net/requirements.txt as well as bcftools http://samtools.github.io/bcftools/ to be able to manipulate vcf files.

There's a first script in smap notebook to create reference.smap from the igsr legend file. This will only keep corresponding supercontinent code in a format like this :

HG00271	EUR 

HG00276	EUR

HG00288	EUR

HG00290	EUR

HG00308	EUR

To run the Lai-Net model, got to ./LAI-Net and take a look at lai_net.ipynb. Example from the original repository are available in ./LAI-Net/notebooks.

Further LAI_NET documentation is available at https://github.com/AI-sandbox/LAI-Net.


# Artificial Data Labelling
Converted vcf files and label generated made by the knn are directly avalaible in data/input/artificial/ folders.

