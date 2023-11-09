import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import os
import pandas as pd
import seaborn as sns

FIGSIZE = None
MARKERSIZE = 100
MAXCOLORS = 8

LAI_PALETTE  = ["#A60303", "#3457BF", "#75BFAA", "#613673",  "#FFA500"]
CMAP = ListedColormap(LAI_PALETTE)

def visualize_palette(label,palette=None):
    if palette is None:
        palette = LAI_PALETTE
    nn = 50
    fig, ax = plt.subplots()

    for i, col in enumerate(palette):
        ax.plot(np.arange(nn), np.repeat(i,nn), color=col, linewidth=20)
    ax.set_yticks([0,1,2,3,4])
    ax.set_yticklabels(label)
    plt.show()



def haplo_tile_plot(haplos, pop_order=None, bbox_to_anchor=[1.2,1.0]):
    """
    Tile plot for visualizing haplotypes.
        - haplos: array of haplotypes
        - pop_order: order of ancestry for figure legend
    """
    ANI_FIGSIZE = (10,2)

    haplos = np.array(haplos, dtype=int)
    n_anc = len(np.unique(haplos))

    n_haplo, n_wind = haplos.shape
    XX = np.array([range(n_wind) for _ in range(n_haplo)]).reshape(-1)
    YY = np.array([np.repeat(i, n_wind) for i in range(n_haplo)]).reshape(-1)
    CC = haplos.reshape(-1)

    fig, ax = plt.subplots(figsize=ANI_FIGSIZE, constrained_layout=True)
    normalize = matplotlib.colors.Normalize(vmin=0, vmax=n_anc)
    scat = ax.scatter(XX, YY, c = CC, marker="s", cmap=CMAP, norm=normalize, s=MARKERSIZE)
    y_ticks_new = ["P" if i%2 else "M" for i in range(n_haplo)]
    y_ticks_new = [tick+"'" if t%4>1 else tick for t, tick in enumerate(y_ticks_new)]
    plt.setp(ax, yticks=range(n_haplo), yticklabels=y_ticks_new)

    if pop_order is not None:
        handles, labels = scat.legend_elements()
        plt.legend(handles, pop_order[np.unique(CC)], loc="upper right", bbox_to_anchor=bbox_to_anchor, title="Ancestry")

    return fig, ax

def plot_cm(cm, normalize=True, labels=None, figsize=(10,8), path=None):
    plt.figure(figsize=figsize)
    
    # normalize w.r.t. number of samples from class
    if normalize:
        row_sums = cm.sum(axis=1)
        row_sums = row_sums.reshape(-1,1)
        with np.errstate(all='ignore'):
            cm = cm / row_sums
        
    df_cm = pd.DataFrame(cm, range(cm.shape[0]), range(cm.shape[1]))
    sns.set(font_scale=1.4) # for label size
    if labels is None:
        fig = sns.heatmap(df_cm, annot=False, annot_kws={"size": 16}) # font size
    else:
        fig = sns.heatmap(df_cm, xticklabels=labels, yticklabels=labels,
                   annot=False, annot_kws={"size": 16}) # font size
    
    plt.show()
    if path is not None:
        fig.figure.savefig(path)

    return fig

def extract_pop_order(output_file):
        # get model population order from first line of file and convert from numeric predictions
    with open(output_file, "r") as f:
        pop = np.array([p.split("=")[0] for p in f.readline().split()[2:]])
        #return the list of the pop in the right order
    return pop
    

def plot_chm(sample_id, msp_df,output_basename,output_file, rm_img=False, img_name="chm_img"):

    """
    Wrapper function for plotting with Tagore. 
    Requires an msp dataframe and a sample_id of which to plot the chromosome.
    """
    
    # defining a color palette
    palette =sns.color_palette(LAI_PALETTE).as_hex()
    
    # get the base of the tagore style dataframe
    nrows = msp_df.shape[0]
    default_params = pd.DataFrame({"feature": [0]*nrows, "size": [1]*nrows})
    tagore_base = msp_df[["#chm", "spos", "epos"]].join(default_params)
    tagore_base.columns = ["chm", "start", "stop", "feature", "size"]
    
    # adding data from the individual with that sample_id
    colors0 = [palette[i] for i in np.array(msp_df[sample_id+".0"])]
    colors1 = [palette[i] for i in np.array(msp_df[sample_id+".1"])]
    tagore0 = tagore_base.join(pd.DataFrame({"color": colors0, "chrCopy": 1}))
    tagore1 = tagore_base.join(pd.DataFrame({"color": colors1, "chrCopy": 2}))
    tagore_df = pd.concat([tagore0, tagore1])
    pop=extract_pop_order(output_file)
    visualize_palette(pop,palette)

    # plot the results
    tagore_df_fname = output_basename+"tagore.tsv"
    tagore_df.to_csv(tagore_df_fname, sep="\t", index=False, 
                     header = ['#chr','spos','epos','feature','size','color','ChrCopy'])
    
    #os.system("tagore --i " + tagore_df_fname + " -p "+ img_name +  " --build hg37 -f")
    print("tagore --i " + tagore_df_fname + " -p "+ img_name +  " --build hg37 -f")
    if rm_img:
        os.system("rm " + tagore_df_fname)
