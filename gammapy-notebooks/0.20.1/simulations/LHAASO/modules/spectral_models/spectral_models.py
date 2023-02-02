#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gammapy.modeling.models import (
    PowerLawSpectralModel,
    ExpCutoffPowerLawSpectralModel,
    LogParabolaSpectralModel,
    SkyModel,
)


# In[ ]:


def pwl_model(index=2,amplitude="1e-12 cm-2 s-1 TeV-1", reference="1 TeV", name ="pwl"):
    
    '''Returns a spectral power-law model
    
    Default function parameters
    ----------
    index=2
    amplitude="1e-12 cm-2 s-1 TeV-1" 
    reference="1 TeV"
    name = None
    ----------
    
    pwl_model(index,amplitude, reference)
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

