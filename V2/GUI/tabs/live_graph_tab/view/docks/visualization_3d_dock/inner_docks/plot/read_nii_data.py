import os
from nibabel import load


def read_nii_data(nii_path):
    # get MRI data
    path = os.path.join(os.getcwd(), nii_path)
    nii = load(path)
    data = nii.get_data()
    return data

