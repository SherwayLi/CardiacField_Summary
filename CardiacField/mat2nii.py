import nibabel as nib
import numpy as np
import scipy.io as sio
import os
import numpy as np

path = os.path.join('/root/CardiacField/2d_example_3d.mat')
mat = sio.loadmat(path) 
gray = np.squeeze(mat['gray'])
new_image = nib.Nifti1Image(gray,np.eye(4))
save_path = os.path.join('/root/CardiacField/putout/save/2d_example_3d.nii')
nib.save(new_image,save_path) 