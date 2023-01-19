#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:25:05 2022

@author: akshay
"""

import detectron2 ,torch,os, json, cv2, random,sys,math,zipfile,shutil

from detectron2.utils.logger import setup_logger
setup_logger()
 
from zipfile import ZipFile
import numpy as np

from matplotlib import pyplot as plt

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.engine import DefaultTrainer

import pandas as pd
from detectron2.utils.visualizer import ColorMode


def getArea(outputs,d,df):
    
    #calculate area
    contours = []
    for pred_mask in outputs["instances"].to("cpu").pred_masks:
        # pred_mask is of type torch.Tensor, and the values are boolean (True, False)
        # Convert it to a 8-bit numpy array, which can then be used to find contours
        mask = pred_mask.numpy().astype('uint8')
        contour, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contours.append(contour[0]) # contour is a tuple (OpenCV 4.5.2), so take the first element which is the array of contour points
    
    img = cv2.imread(d)
    
    color=(255, 0, 0)
    #box=outputs["instances"].to("cpu").pred_boxes.tensor.numpy()
    for i in range(len(contours)):
        item=contours[i]
        
        ###########
        #intetnsity
        ###########
        cimg = np.zeros_like(img)
        cv2.drawContours(cimg, contours, i, color=255, thickness=-1)
        # Access the image pixels and create a 1D numpy array then add to list
        pts = np.where(cimg == 255)
        inten=round(np.mean(img[pts[0], pts[1]]),2)
        
        ###########
        #area
        ###########

        cv2.polylines(img, [item], True,color , 3)
        area_cm=cv2.contourArea(item)
        
        #update dataframe
        df.loc[len(df)] = [d.split("/")[-1], i,area_cm,inten] 
        
        cv2.putText(img, "SN:{}->{}".format(i,area_cm), (int(item[0][0][0]), int(item[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (192, 245, 162) , 5)
    return img





def predict(imagesPath,thr,imageType): 

    if imageType=="incucyte":
        weight="model_final_Incu.pth"
    else:
        weight="model_final.pth"
    
    
    cfg = get_cfg()
    cfg.MODEL.DEVICE='cpu'

    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.SOLVER.IMS_PER_BATCH = 4 
    cfg.SOLVER.MAX_ITER = 500
    cfg.SOLVER.STEPS = []        
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 256 
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.WEIGHTS = os.path.join(weight)  # path to the model we just trained   
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = thr   # set a custom testing threshold
    predictor = DefaultPredictor(cfg)


    filenames=os.listdir(imagesPath)
    os.chdir(imagesPath)
    
    areaData = pd.DataFrame(columns=['filename',"spheroid No" ,'area (in pixels)', 'intensity'])
    
    for d in filenames: 
        if not any(d.endswith(s) for s in [".jpeg",".tif",".jpg"]):
            continue
        im = cv2.imread(d)
        outputs = predictor(im)  
        v = Visualizer(im[:, :, ::-1], 
                       scale=0.5,
                       instance_mode=ColorMode.IMAGE_BW   
        )
               
        cv2.imwrite(d, getArea(outputs,d,areaData)) 
        
    areaData.sort_values(by=["filename"],inplace=True)
    areaData.to_csv('spheroidArea.csv')  

    with ZipFile("results.zip", 'w') as zipObj2:
        for d in filenames: 
            if not any(d.endswith(s) for s in [".jpeg",".tif",".jpg"]):
                continue
            zipObj2.write(d) 
        zipObj2.write("spheroidArea.csv")
        

    
    shutil.copyfile("results.zip", "/".join(os.getcwd().split("/")[:-1])+"/results.zip")
 
    cwd="/".join(os.getcwd().split("/")[:-1])
    os.chdir(cwd)

    for file in [ f for f in os.listdir("./") if not f.endswith('.zip')]:
        if file.startswith('.'):
            continue
        shutil.rmtree(file)
        
    cwd="/".join(os.getcwd().split("/")[:-2])
    os.chdir(cwd)
    


    