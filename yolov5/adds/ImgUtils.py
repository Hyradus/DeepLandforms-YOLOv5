#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: ImgUtils module containing various function for manipulate images
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Mon Oct 12 16:47:44 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""
import os
import numpy as np
import cv2 as cv
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import rasterio as rio
from rasterio.plot import reshape_as_raster
from adds.inf2shp import get_world_file, getAffine

def ImgWriter(save_name, img, img_crs, tile_transform, ext, f1):
    if ext == 'tiff':
        drv = 'GTiff'
    elif ext == 'png':
        drv='PNG'
    elif ext == 'jpg':
        drv='JPEG'
    if f1 ==1:
        cnt = img.shape[0]
        drv='GTiff'
        sname = save_name+'tiff'
    else:
        try:
            cnt=img.shape[2]
        except:
            cnt=1
        sname = save_name+ext
    if cnt ==1:
        h=0
        w=1
    else:
        h=1
        w=2
    with rio.open(sname, 'w',
                              driver = drv,
                              height= img.shape[h],
                              width=img.shape[w],
                              count=cnt,
                              dtype=img.dtype,
                              crs=img_crs,
                              transform=tile_transform) as dst:
                    if f1==1:
                        dst.write(img)
                    else:
                        dst.write(img,cnt)


         
def InfImgWriter(source, save_path, image):
    
    basename = os.path.basename(save_path)
    split = basename.split('.')
    ext = split[len(split)-1]
    src_basename = source + '/'+split[0]
    src_image = src_basename+'.'+ext    
    im = rio.open(src_image)
    img_crs = im.crs
    trs = im.transform
    if img_crs == None:
        img_crs=checkCRS(src_basename)
    if trs == None:
        trs=checkAffine(ext, src_basename)
    if img_crs and trs != None:
        imm = reshape_as_raster(image)
        savename = save_path.split(ext)[0]
        ImgWriter(savename, imm, img_crs, trs, ext,1)
    
def checkCRS(src_basename):
     crs_file=src_basename+'.wkt'
     try:
         with open(crs_file, "r") as f:
             crs_file=src_basename+'.wkt'
             with open(crs_file, "r") as f:
                 img_crs = f.read()
                 return(img_crs)
     except Exception as e:
            #print(e)
            print('Missing  ', src_basename, ' file, skipping.')
            img_crs=None
            
            return(img_crs)

def checkAffine(ext, src_basename):
    try:
        _,wrf=get_world_file(ext)
        world_file = src_basename+wrf
        trs=getAffine(world_file)
        return(trs)
    except Exception as e:
        print(e)
        print('Skipping: ', src_basename)
        trs = None
        return(trs)

                         
def Area(chkImage):
    try:
        chkImg = Image.fromarray(chkImage)
    except:
        chkImg = chkImage
        
    width, height = chkImg.size
    area = width*height
    return(area)

def ImageBorderErode(image, pixels):
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image)
    width, height = img.size
    left = pixels
    top = pixels
    right = width-pixels
    bot = height-pixels
    img_precrop= img.crop((left, top, right, bot))
    im = np.array(img_precrop)
    return(img_precrop, im)                

def CvContourCrop(processed_image):
    _, threshold = cv.threshold(processed_image, 1, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    x, y, w, h = cv.boundingRect(best_cnt)
    img_crop = processed_image[y:y+h, x:x+w]
    return(img_crop)

def maxRectContourCrop(processed_image):
    _, bins = cv.threshold(processed_image, 1, 255, cv.THRESH_BINARY)
    bins = cv.dilate(bins, None)
    bins = cv.erode(bins, None)
    contours, hierarchy = cv.findContours(bins, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    from maxrect import get_intersection, get_maximal_rectangle
    coords = coordFinder(contours, processed_image)
    _, coordinates = get_intersection([coords])
    coo = list(coordinates)
    ll, ur = get_maximal_rectangle(coo)
    bx = (ll[0],ll[1],ur[0],ur[1])
    image = Image.fromarray(processed_image)
    img_crop = image.crop(bx)  
    return(img_crop)

def coordFinder(contours, gray):
    for cnt in contours : 
        approx = cv.approxPolyDP(cnt, 0.009 * cv.arcLength(cnt, True), True) 
        n = approx.ravel()  
        i = 0
        coords =[]
        for j in n : 
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 
                # String containing the coordinates. 
                coords.append([int(x),int(y)])
            i = i + 1
    return(coords)
           
def imgNorm(image, image_dir, name):
    import cv2 as cv
    image_norm= cv.normalize(image, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    name_norm=image_dir+name+'_normalized.png'
    cv.imwrite(name_norm,image_norm)
    return(image_norm)

def imgScaler(image, image_dir,name):
    from sklearn import preprocessing 
    min_max_scaler = preprocessing.MinMaxScaler()
    img_norm = (min_max_scaler.fit_transform(image)*255).astype(np.uint8)
    name_scal = image_dir+name+'_scaled.png'
    cv.imwrite(name_scal, img_norm)
    
def imgDen(image, image_dir, name):
    import cv2 as cv
    image_den = cv.fastNlMeansDenoising((image).astype(np.uint8), None, 10,7,21)
    name_den=name+'_denoised.png'
    cv.imwrite(name_den, image_den)

def imgEnh(image, name):
    if isinstance(image, list):
        img_norm = []
        for im in image:
            img_norm.append(cv.normalize(im, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX))
        img_merge=(img_norm[0]+img_norm[1])*2
        cv.imwrite('Merged2.png',img_merge)
