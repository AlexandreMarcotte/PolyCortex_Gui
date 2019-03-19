import numpy as np


def write_to_file(gv):
    with open(gv.save_path, 'w') as f:
        # Create the proper dimension for the concatenation
        all_t = np.array(gv.all_t)[None, :]
        all_experiment_val = np.array(gv.all_experiment_val)[None, :]

        # Make sure all data have the same length
        len_each_data = len(gv.all_data[0]) ,len(all_t[0]), len(all_experiment_val[0])
        print(len_each_data)
        min_len = min(len_each_data )
        all_data = gv.all_data[:min_len]
        all_t = all_t[:min_len]
        all_experiment_val = all_experiment_val[:min_len]

        # Concatenate
        save_val = np.concatenate((all_data, all_t, all_experiment_val))
        # Save
        print('Data save to: ', f)
        np.savetxt(f, np.transpose(save_val), delimiter=',')