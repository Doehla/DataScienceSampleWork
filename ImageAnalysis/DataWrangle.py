import os
import sys
import PIL
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# set up options
np.set_printoptions(threshold=sys.maxsize, linewidth=np.inf, precision=3)


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


def transform_image_data(img_data):
    dim_count = (
        150,
        150,
        3  # channels
    )
    shape_data = img_data.shape

    def extract_middle(idx):
        x_lower =   int(np.floor((shape_data[idx] - dim_count[idx]) / 2))
        x_upper = -1*int(np.ceil((shape_data[idx] - dim_count[idx]) / 2))
        # TODO: It would be great to generalize this part too...
        if idx == 0:
            img_altered = img_data[x_lower:x_upper,:,:]
        elif idx == 1:
            img_altered = img_data[:,x_lower:x_upper,:]
        ## end todo
        return img_altered

    def append_average(idx):
        # add to the image using the average of the data in the associated row
        img_altered = img_data
        fill_values = np.divide(np.sum(img_data, axis=idx), shape_data[idx]).astype(int)
        # TODO: It would be great to generalze this part too...
        x_shape = fill_values.shape
        if idx == 0:
            x_shape = (1, x_shape[0], x_shape[1])
        elif idx == 1:
            x_shape = (x_shape[0], 1, x_shape[1])
        ## end todo
        fill_values = np.reshape(fill_values, x_shape)
        for _ in range(dim_count[idx] - shape_data[idx]):
            img_altered = np.append(img_altered, fill_values, axis=idx)
        return img_altered

    # If the shape of the image is not as expected, change it to that expected
    if not (shape_data == dim_count):
        if not (shape_data[2] == dim_count[2]):
            # Not 3 channel. This is a larger issue.
            img_data = None
        else:
            for i in range(2):
                if shape_data[i] > dim_count[i]:
                    img_data = extract_middle(i)
                elif shape_data[i] < dim_count[i]:
                    img_data = append_average(i)

    # Image data has values from 0 to 255. Convert these to [0,1]
    img_data = img_data/255

    return img_data


def construct_file_df(dir_path, include_labels=False, output_file=None):
    """Construct a dataframe with file_path
        and optionally the label of the file.
    WARNING: This does not consider memory limitations and will attempt to return everything.
    """
    if (output_file is not None) and os.path.isfile(output_file):
        os.remove(output_file)
        print('removed old file')

    first_print = True
    data = []
    cols = ['file_path']
    if include_labels:
        cols.append('file_label')
    cols.append('file_img')

    def write_to_file(use_data, p_head):
        df = pd.DataFrame(use_data, columns=cols)
        df.to_csv(f_output, index=False, mode='a', header=p_head)
        with open(f_output, 'r') as f:
            cnt = sum(1 for _ in f)
        print('Wrote batch {} -> {} ({})'.format(df.shape, cnt, f_output))

    for i, file in enumerate(fetch_contents(dir_path)):
        data_elem = dict()
        data_elem['file_path'] = file

        if include_labels:
            # Take advantage of knowing that we use the folder the file is directly in for the label of the file
            label = os.path.split(os.path.split(file)[0])[1]
            data_elem['file_label'] = label

        img = mpimg.imread(file)
        img = transform_image_data(img)
        data_elem['file_img'] = img.ravel()
        data.append(data_elem)

        if (output_file is not None) and (i % 50 == 0):
            write_to_file(data, first_print)
            data = []
            first_print = False

    if (output_file is not None):
        write_to_file(data, first_print)
        df = None
    else:
        df = pd.DataFrame(data, columns=cols)

    return df


if __name__ == '__main__':
    loop_vars = [
        ('seg_train', 'training_data.csv', True),
        ('seg_test', 'test_data.csv', True),
        ('seg_pred', 'predict_data.csv', False)
    ]

    for folder, file, labeled in loop_vars:
        print('Processing: {}'.format(file))
        f_root = os.path.dirname(os.path.abspath(__file__))
        f_data_folder = os.path.join('data', folder)
        f_data_root = os.path.join(f_root, f_data_folder)
        f_output = os.path.join(f_root, 'data', 'packaged', file)

        df = construct_file_df(
            f_data_root,
            include_labels=labeled,
            output_file=f_output
        )
    print('Done!')
