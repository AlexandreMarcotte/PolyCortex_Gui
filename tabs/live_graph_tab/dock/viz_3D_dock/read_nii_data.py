import os
from nibabel import load


def read_nii_data(nii_path):
    # get MRI data
    nii = load(os.path.join(os.getcwd(), nii_path))
    data = nii.get_data()
    return data

