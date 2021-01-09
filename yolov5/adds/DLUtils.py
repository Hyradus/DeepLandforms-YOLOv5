#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Dec 28 17:02:24 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import os
from adds.GenUtils import make_folder
from datetime import datetime

def get_classes(file):
    with open(file,'r') as f:
        for line in f:
            if 'nc:' in line:
                cls_num = line.split(':')[1]
            if 'names:' in line:
                cls_names = line.split(':')[1]
        return(cls_num, cls_names)                
    
    
def get_model_cfg(source, models_folder, q):
    weights_folder = make_folder(source, 'trained_weights')
    if q == 1:
        name = 'yolov5s.yaml'
        model = models_folder+'/'+name
        weights = weights_folder+'/custom_'+name.split('.')[0]+'.pt'
    elif q == 2:
        name = 'yolov5m.yaml'
        model = models_folder+'/'+name
        weights = weights_folder+'/custom_'+name.split('.')[0]+'.pt'
    elif q == 3:
        name = 'yolov5l.yaml'
        model = models_folder+'/'+name
        weights = weights_folder+'/custom_'+name.split('.')[0]+'.pt'
    elif q == 4:
        name = 'yolov5x.yaml'
        model = models_folder+'/'+name
        weights = weights_folder+'/custom_'+name.split('.')[0]+'.pt'
    return(model, weights, name.split('.yaml')[0])


def cfg_class(source, model_cfg_file, num_class):
    import os
    
    fin = open(model_cfg_file,'rt')
    # new_cfg = os.path.dirname(model_cfg_file)+'/custom_'+os.path.basename(model_cfg_file)
    new_cfg = source+'/custom_'+os.path.basename(model_cfg_file)
    fout = open(new_cfg,'wt')
    
    for line in fin:
        if line.startswith('nc:'):
            line = 'nc: '+str(num_class)+'\n'
            fout.write(line)
        else:
            fout.write(line)
    fin.close()
    fout.close()
    return(new_cfg)

def get_train_cfg(source, data_yaml, models_folder, q):
    if q == 1:
        name = 'yolov5s.yaml'
        model = models_folder+'/'+name
    elif q == 2:
        name = 'yolov5m.yaml'
        model = models_folder+'/'+name
    elif q == 3:
        name = 'yolov5l.yaml'
        model = models_folder+'/'+name
    elif q == 4:
        name = 'yolov5x.yaml'
        model = models_folder+'/'+name
    num_class, cls_names = get_classes(data_yaml)
    now = datetime.now()
    folder = now.strftime("%d-%m-%Y_%H-%M-%S")
    run_folder = make_folder(source,folder)
    cfg_file = cfg_class(run_folder, model, num_class)
    return(cfg_file, name.split('.yaml')[0],folder)

def get_args(args_dict):
    import shlex
    arvs= []
    for arg in args_dict.keys():
        ii = args_dict[arg]
        if  type(ii)==bool:
            arvs.append(arg)
        elif ii !='':
            arvs.append(arg)
            arvs.append(str(ii))
    arv = ' '.join(shlex.quote(arg) for arg in arvs)
    return(arv)

def link_dataset(home, source):
    train = '/train'
    valid = '/valid'
    train_src = source+train
    #train_dst = os.path.dirname(home)+train
    train_dst = home+train
    valid_src = source+valid
    valid_dst = home+valid
    #valid_dst = os.path.dirname(home)+valid
    os.symlink(train_src, train_dst, target_is_directory=True)
    os.symlink(valid_src, valid_dst, target_is_directory=True)