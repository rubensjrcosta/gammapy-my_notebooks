#!/usr/bin/env python
# coding: utf-8

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


# In[ ]:


from gammapy.catalog import CATALOG_REGISTRY # Registry of source catalogs in Gammapy.
def load_gammapy_catalogs(print_catalogs = False):
    '''To write Docstring!!!!'''
    catalogs_cls = []

    catalog_gammacat = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[0])()
    catalogs_cls.append(catalog_gammacat)

    catalog_hgps = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[1])()
    catalogs_cls.append(catalog_hgps)

    catalog_2hwc = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[2])()
    catalogs_cls.append(catalog_2hwc)

    catalog_3hwc = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[3])()
    catalogs_cls.append(catalog_3hwc)

    catalog_3fgl = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[4])()
    catalogs_cls.append(catalog_3fgl)

    catalog_4fgl = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[5])()
    catalogs_cls.append(catalog_4fgl)

    catalog_2fhl = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[6])()
    catalogs_cls.append(catalog_2fhl)

    catalog_3fhl = CATALOG_REGISTRY.get_cls(cfg.catalogs_tags[7])()
    catalogs_cls.append(catalog_3fhl)
    
    if print_catalogs:
        for catalog in catalogs_cls:
            print(f"{catalog}")
    
    return catalogs_cls


# In[ ]:


from pathlib import Path


# In[ ]:


def mkdir_sub_directory(parent_directory = None, child_directory = None):
    '''Creates a directory: parent_directory/child_directory and returs the path 
    >>>mkdir_sub_directory(parent_directory, directory)
    path_parent, path_child
    '''
    if child_directory is None:

        path_parent = Path(f"{parent_directory}")
        path_parent.mkdir(exist_ok=True)
        print("Directory '% s' created" % path_parent)
        
        return path_parent
    
    else:
        
        path_parent = Path(f"{parent_directory}")
        path_parent.mkdir(exist_ok=True)

        path_child = Path(f"{path_parent}/{child_directory}")
        path_child.mkdir(parents=True, exist_ok=True)
        print("Directory '% s' created" % path_child)

        return (path_parent, path_child)


# In[ ]:


def name_to_txt(name):
    '''Given a `string`, `find` and `replace` the space by "_" and . by "dot"
    >>> name_to_txt(n ame.)
    namedot
    '''
    return name.replace(" ", "_").replace(".", "dot").replace(":", "_")


# In[ ]:





# In[ ]:


def number_to_txt(num):
    '''Given a `number`, return a string
    >>> number_to_txt(num = 1.002222):
    1
    '''
    return ("%.2f" % num).rstrip('0').rstrip('.').replace(".", "dot")
    


# In[ ]:





# In[1]:


# path_fp_t_LHAASO = "/home/born-again/Documents/GitHub/grupo_AAE/data_access_and_selection(DL3)/flux_points_tables/LHASSOColaboration_publishNature_2021"
from astropy.table import Table
from astropy import units as u
def LHAASO_table_to_SED_format(path, file_name):
    '''
    Normalization Representation
    The SED format is a flexible specification for representing one-dimensional spectra 
    (distributions of amplitude vs. energy).
    
    '''
    
    format_dat = '.dat'
    file_path = Path(f'{path}/{file_name}{format_dat}') 

    table = Table.read(file_path,format='ascii', delimiter=' ', comment='#')
    
#     display(table)

    table['col1'] = table['col1']/1e12
    table.rename_column('col1', 'e_ref')
    table['e_ref'].unit = u.TeV

    #     table['col5'] = table['col5']/1e12
    #     table.rename_column('col5', 'e_min')
    #     table['e_min'].unit = u.TeV

    #     table['col6'] = table['col6']/1e12
    #     table.rename_column('col6', 'e_max')
    #     table['e_max'].unit = u.TeV

    table.rename_column('col2', 'e2dnde')
    table['e2dnde'].unit = u.Unit("erg cm-2 s-1")

    table.rename_column('col3', 'e2dnde_errp')
    table['e2dnde_errp'].unit = u.Unit("erg cm-2 s-1")

    table.rename_column('col4', 'e2dnde_errn')
    table['e2dnde_errn'].unit = u.Unit("erg cm-2 s-1")

    table.meta["SED_TYPE"] = "e2dnde"
    table.meta["name"] = "table"
    table.remove_columns(['col5', 'col6'])

    display(table)
    
    return table


# In[ ]:





# In[ ]:


import sys, os
format_fits = '.fits'

def write_tables_csv(table, path_file, file_name):
# Writes the flux points table in the csv format
    path_os = os.path.abspath(
        os.path.join(
            f"{path_file}/{file_name}{cfg.format_csv}"
        )
    )

    if path_os not in sys.path:
        sys.path.append(path_os)

    table.write(
        f"{path_os}",
        format = 'ascii.ecsv', 
        overwrite = True
    )   
    return


# In[ ]:


import sys, os
format_fits = '.fits'

def write_tables_fits(table, path_file, file_name):
    # Writes the flux points table in the fits format
    path_os = os.path.abspath(
        os.path.join(
            f"{path_file}/{file_name}{cfg.format_fits}"
        )
    )      

    if path_os not in sys.path:
        sys.path.append(path_os)

    table.write(
        f"{path_os}",
        format = 'fits', 
        overwrite = True
    )   
    return


# In[ ]:




