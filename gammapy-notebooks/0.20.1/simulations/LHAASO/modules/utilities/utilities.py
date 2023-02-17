#!/usr/bin/env python
# coding: utf-8

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

