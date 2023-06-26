#!/usr/bin/env python
# coding: utf-8

# [gammapy.modeling.models.SpectralModel](https://docs.gammapy.org/1.0/api/gammapy.modeling.models.SpectralModel.html#gammapy.modeling.models.SpectralModel)

# In[ ]:


import os
import sys
import importlib

path_modules = '../my_modules'

module_path = os.path.abspath(f'{path_modules}/config')
if module_path not in sys.path:
    sys.path.append(module_path)

import cfg
importlib.reload(cfg)


# In[3]:


from gammapy.modeling.models import (
    PowerLawSpectralModel,
    ExpCutoffPowerLawSpectralModel,
    LogParabolaSpectralModel,
    SkyModel,
)
from astropy import units as u


# In[4]:


def pwl_model(index=2,amplitude="1e-12 cm-2 s-1 TeV-1", reference=1 * u.TeV, name = "pwl"):
    
    '''Returns a spectral power-law model
    
    Default function parameters
    ----------
    index=2
    amplitude="1e-12 cm-2 s-1 TeV-1" 
    reference="1 TeV"
    name = None
    ----------
    
    pwl_model(index, amplitude, reference)
    >>> model 
     '''
    spec_model = PowerLawSpectralModel(
        index=index, 
        amplitude=amplitude, 
        reference=reference
    )
    sky_model = SkyModel(
    spectral_model=spec_model, 
    name= name
    )
    return spec_model, sky_model


# In[ ]:





# In[6]:


def lp_model(alpha=2.0, amplitude="1e-12 cm-2 s-1 TeV-1", reference=1 * u.TeV, beta=1.0, name = "lp"):
    
    '''
    
     '''
    spec_model =  LogParabolaSpectralModel(
        alpha=alpha,
        amplitude=amplitude,
        reference=reference,
        beta=beta,
    )
    sky_model = SkyModel(
        spectral_model=spec_model, 
        name= name
    )
    return spec_model, sky_model


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


import pandas as pd 
from gammapy.datasets import FluxPointsDataset
from gammapy.catalog import CATALOG_REGISTRY
import os
import sys

# format_csv = ".csv"
format_fits = ".fits"

sed_type="e2dnde"

lst=[]
ds_lst = []

def get_source_data(dict_lhaaso_tevc = None, catalog_tags = None, path_dir = None):
    
    i_range = range(len(dict_lhaaso_tevc.keys()))
    for i in i_range:

        LHAASO_name = list(dict_lhaaso_tevc.keys())[i]
        LHAASO_id = LHAASO_name.replace(" ", "")
        
        j_range = range(len(dict_lhaaso_tevc[LHAASO_name]))
        for j in j_range:

            catalog_src = []

            pf_on = []
            src_on = []

            ds_j=[]

            source_name=dict_lhaaso_tevc[LHAASO_name][j]
            source_id = source_name.replace(" ", "")
            
            k_range = range(len(catalog_tags))
            for k in k_range: 
                
                catalog_tag = catalog_tags[k]
                catalog=CATALOG_REGISTRY.get_cls(catalog_tag)()
                
                try:
                    
                    src=catalog[source_name]
                    src_on.append(src.data)
                    catalog_src.append(catalog_tag)
                    
                    ds = FluxPointsDataset(
                        data=src.flux_points, 
                        name=catalog_tag
                    )
                    
                    ds_j.append(ds)
                    pf_on.append(catalog_tag)

                    table = ds.data.to_table(
                        sed_type=sed_type, 
                        formatted=True
                    )

                    file_name = f'{LHAASO_id}_{source_id}_{catalog_tag}{format_fits}'
                    path_os = os.path.abspath(
                        os.path.join(
                            f"{path_dir}/{file_name}"
                        )
                    )
                    
                    
                    if path_os not in sys.path:
                        sys.path.append(path_os)

                    #table.write(f"{path_os}{format_csv}",format='ascii.ecsv', overwrite=True)
                    table.write(f"{path_os}",format='fits', overwrite=True)
                    
                except:
                    pass

                lst_k=[LHAASO_name, source_name, catalog_src, pf_on, ds_j, src_on]
            lst.append(lst_k)
            ds_lst.append(ds_j)

    df = pd.DataFrame(lst, columns =['LHAASO', 'TeV Conterpart', 'Catalog', 'Flux Points', 'ds', 'src']) 
    df.to_csv(f"{path_dir}/flux_points.csv", index = True )
    return df, ds_lst

