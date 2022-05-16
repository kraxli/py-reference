
liabilities_df = pd.DataFrame(liabilities, index=balance_sheets, columns=seniority_classes)
liabilities_df.index.names = ['fsa']
liabilities_df.columns.names = ['seniority_class']
liabilities_df.head()
liabilities_df.query("fsa=='324'")
liabilities_df = pd.DataFrame(liabilities_df.stack(), columns=['trx'])
liabilities_df['internal'] = 0
liabilities_df['counterparty'] = -9999
liabilities_df.set_index(['internal', 'counterparty'], append=True, inplace=True)
# liabilities_df.loc[("324")]
liabilities_df.query("fsa=='324'")


# method for old mat file format:
from scipy.io import loadmat

file_old_mat_format = "file_old_mat_format.mat"
loadmat(file_old_mat_format)


# method for new mat-file formats (v7.3 and beyond):

## method 1
import h5py

# with h5py.File(file_v73, 'r') as f:
#     f.keys() 

f = h5py.File(file_v73, 'r') 
arrays = {}
for k, v in f.items():
    arrays[k] = np.array(v)
    
print( arrays )

## method 2

import mat73
#    See also hdf5storage, which can indeed be used for saving .mat, but has less features for loading than mat73
data_dict = mat73.loadmat(file_v73)
print(data_dict)

# old / new mat-file formats:

import hdf5storage
mat = hdf5storage.loadmat(file_v73)    
mat

# matlab tables cannot be read from a mat-file it seems (one needs to save it as struct or to csv)
