import os
import PIL
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def fetch_contents(dir_path):
    """Generator function to return all files found under the given file folder.
    This does look into subfolders. Returned values are the absolute file paths.
    """
    for x in os.listdir(dir_path):
        x_path = os.path.join(dir_path, x)
        if os.path.isdir(x_path):
            yield from fetch_contents(x_path)
        else:
            yield x_path


def construct_file_df(dir_path, include_labels=False):
    """Construct a dataframe with file_path
        and optionally the label of the file.
    WARNING: This does not consider memory limitations and will attempt to return everything.
    """
    data = []
    cols = ['file_path', 'file_img']
    if include_labels:
        cols.append('file_label')

    for i, file in enumerate(fetch_contents(dir_path)):
        data_elem = dict()
        data_elem['file_path'] = file

        if include_labels:
            # Take advantage of knowing that we use the folder the file is directly in for the label of the file
            label = os.path.split(os.path.split(file)[0])[1]
            data_elem['file_label'] = label

        img = mpimg.imread(file)
        data_elem['file_img'] = img
        data.append(data_elem)

    df = pd.DataFrame(data, columns=cols)
    return df






if __name__ == '__main__':
    f_root = os.path.dirname(os.path.abspath(__file__))
    f_data_folder = os.path.join('data', 'seg_train')
    f_data_root = os.path.join(f_root, f_data_folder)
    f_output = os.path.join(f_root, 'data', 'packaged', 'training_data.csv')

    df = construct_file_df(f_data_root, include_labels=True)
    df.to_csv(f_output, index=False)

    print(df.info())
