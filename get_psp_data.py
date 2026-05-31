import cdflib
import numpy as np
from pyspedas.projects.psp import fields

print("Downloading PSP data...")
cdf_files = fields(trange=['2024-01-01', '2024-01-02'], datatype='mag_rtn', level='l2', downloadonly=True)

print("Extracting arrays directly from CDF files...")
all_times = []
all_vectors = []

for file in sorted(cdf_files):
    cdf = cdflib.CDF(file)
    z_vars = cdf.cdf_info().zVariables
    
    # Dynamically find the primary data variable
    mag_var = next(v for v in z_vars if 'mag_rtn' in v.lower() and 'quality' not in v.lower() and 'epoch' not in v.lower())
    
    # Dynamically find the associated time (epoch) variable, bypassing the broken varinq() lookup entirely
    epoch_var_name = next(v for v in z_vars if 'epoch' in v.lower() and 'mag_rtn' in v.lower())
    
    epochs = cdf.varget(epoch_var_name)
    times = cdflib.cdfepoch.unixtime(epochs)
    vectors = cdf.varget(mag_var)
    
    all_times.append(times)
    all_vectors.append(vectors)

final_times = np.concatenate(all_times)
final_vectors = np.concatenate(all_vectors)

print(f"Successfully loaded {len(final_times)} raw data points.")
print("First data vector (R, T, N in nT):", final_vectors[0])

# The final_times and final_vectors arrays are now fully ready for your equations
