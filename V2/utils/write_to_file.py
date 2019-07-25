# --General Packages--
import numpy as np
import os
# -- My Packages --
from V2.general_settings import GeneralSettings


def append_to_file(
        all_data=[], all_t=[],
        all_experiment_val=[],
        first_save=True,
        save_path=GeneralSettings.save_path):

    all_data = np.array(all_data)
    all_t = np.array(all_t)
    all_experiment_val = np.array(all_experiment_val)
    # TODO: ALEXM:
    # WARNING: block if your read from the same file you save in
    # EVALUATE IF THE SAVE AND READ FILE ARE THE SAME:
    # IF YES THROW AN ERROR
    save_path = os.path.join(save_path, 'TEST_save.csv')

    if first_save:
        write_type = 'w'
    else:
        write_type = 'a'

    with open(save_path, write_type) as f:
        # Create the proper dimension for the concatenation
        all_t = np.array(all_t)[None, :]
        all_experiment_val = np.array(all_experiment_val)[None, :]

        # Make sure all data have the same length
        len_each_data = len(all_data[0]), len(all_t[0]), len(all_experiment_val[0])
        print(len_each_data)
        min_len = min(len_each_data)
        all_data = all_data[:min_len]
        all_t = all_t[:min_len]
        all_experiment_val = all_experiment_val[:min_len]

        # Concatenate
        save_val = np.concatenate((all_data, all_t, all_experiment_val))
        # Save
        np.savetxt(f, np.transpose(save_val), delimiter=',')
