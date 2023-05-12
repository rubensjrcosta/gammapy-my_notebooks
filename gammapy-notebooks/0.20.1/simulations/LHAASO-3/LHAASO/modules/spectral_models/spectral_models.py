#!/usr/bin/env python
# coding: utf-8

# [gammapy.modeling.models.SpectralModel](https://docs.gammapy.org/1.0/api/gammapy.modeling.models.SpectralModel.html#gammapy.modeling.models.SpectralModel)

# In[ ]:


from gammapy.modeling.models import (
    PowerLawSpectralModel,
    ExpCutoffPowerLawSpectralModel,
    LogParabolaSpectralModel,
    SkyModel,
)


# In[ ]:


def pwl_model(index=2,amplitude="1e-12 cm-2 s-1 TeV-1", reference="1 TeV", name = "pwl"):
    
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

def get_source_data(TeVCount_dict = None, catalog_tags = None, path_dir = None):
    
    i_range = range(len(TeVCount_dict.keys()))
    for i in i_range:

        LHAASO_name = list(TeVCount_dict.keys())[i]
        LHAASO_id = LHAASO_name.replace(" ", "")
        
        j_range = range(len(TeVCount_dict[LHAASO_name]))
        for j in j_range:

            catalog_src = []

            pf_on = []
            src_on = []

            ds_j=[]

            source_name=TeVCount_dict[LHAASO_name][j]
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


# In[ ]:


def _model(index=2,amplitude="1e-12 cm-2 s-1 TeV-1", reference="1 TeV", name = "pwl"):

    log_parabola = LogParabolaSpectralModel(
    alpha=2, amplitude="1e-12 cm-2 s-1 TeV-1", reference="1 TeV", beta=0.1
    )
    model = SkyModel(spectral_model=log_parabola, name="j1507-lp")

