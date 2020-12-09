#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Wed Dec  2 21:44:14 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import os
import shutil
import datetime

def question(question, answers):
    answ = None
    while answ not in answers:
        print('Please enter only: ')
        print(*answers, sep=', ')
        
        answ = input('\n'+question+'  Answer: ')
    return(answ)

def make_folder(path, name):
    folder = path+'/'+name
    if os.path.exists(folder):
           qst = name + ' Folder exist, remove it? '
           answ = question(qst,['yes','y','no','n'])
           if answ in ['yes', 'y']:
               shutil.rmtree(folder)
               os.mkdir(folder)
               print(name, 'Folder created')
           else:
               now = datetime.now()
               folder = name +'_' + now.strftime("%d-%m-%Y_%H-%M-%S")
               print(folder, ' Folder not exist, creating.')
               os.mkdir(folder)
               print('Created new ', name,' Folder')
    else:
        print(name, ' Folder not exist, creating.')
        os.mkdir(folder)
        print('Created new ', name,' Folder')
    return(folder)

def get_paths(PATH, ixt):
    import re
    import fnmatch
    os.chdir(PATH)
    ext='*.'+ixt
    chkCase = re.compile(fnmatch.translate(ext), re.IGNORECASE)
    files = [f for f in os.listdir(PATH) if chkCase.match(f)]
    return(files)

def get_types(folder):
    files  = get_paths(folder, '*')
    types = []
    for f in files:
        types.append(f.split('.')[1])
    uni_vals = set(types)
    return(uni_vals)

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
    return(model, weights)


def cfg_class(model_cfg_file, num_class):
    import os
    
    fin = open(model_cfg_file,'rt')
    new_cfg = os.path.dirname(model_cfg_file)+'/custom_'+os.path.basename(model_cfg_file)
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
    model_cfg_file, weights = get_model_cfg(source, models_folder, q)
    num_class, cls_names = get_classes(data_yaml)
    cfg_file = cfg_class(model_cfg_file, num_class)
    return(cfg_file, weights)

def get_args(args_dict):
    import shlex
    arvs= []
    for arg in args_dict.keys():
        if args_dict[arg] == True:
            arvs.append(arg)
        if args_dict[arg] and args_dict[arg] != True:
            arvs.append(arg)
            arvs.append(str(args_dict[arg]))
            
    arv = ' '.join(shlex.quote(arg) for arg in arvs)
    return(arv)

def link_dataset(home, source):
    train = '/train'
    valid = '/valid'
    train_src = source+train
    train_dst = os.path.dirname(home)+train
    valid_src = source+valid
    valid_dst = os.path.dirname(home)+valid
    os.symlink(train_src, train_dst, target_is_directory=True)
    os.symlink(valid_src, valid_dst, target_is_directory=True)
