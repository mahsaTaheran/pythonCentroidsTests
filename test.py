# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 14:01:20 2019

@author: mtaheran
"""
import os
import glob
from astropy.io import fits
import centroids as centr
import numpy as np
from astropy import stats
from multiprocessing import Pool
import photutils
from scipy import signal
from matplotlib import ticker
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib import rcParams

def test_stack():
    Images=glob.glob('C:\\Users\\mtaheran\\Documents\\MATLAB\\centroiding\\Selected\\*.fits')
    Cubeimg=[]
    for img in Images:
        Cubeimg.append(fits.open(img)[0].data)     
    Img_array=np.array(Cubeimg)
    fits.writeto('C:\\Users\\mtaheran\\Documents\\MATLAB\\centroiding\\Selected\\Cubeimg\\Cubeimg.fits',Img_array)   
#    fits.close('C:\\Users\\mtaheran\\Documents\\MATLAB\\centroiding\\Selected\\Cubeimg\\Cubeimg.fits')
    with fits.open('C:\\Users\\mtaheran\\Documents\\MATLAB\\centroiding\\Selected\\Cubeimg\\Cubeimg.fits') as input:
        C=centr.get_centroids(input[0].data,removeconst=False)
        imgs_bgremoved=centr.remove_background(input[0].data)
        print(input[0].data.shape)
        mean,median,std = stats.sigma_clipped_stats(input[0].data[0,:,:],
                                                sigma=3.0,
                                                maxiters=2,
                                                cenfunc='median')
        threshold=0.99
        bg_threshold=threshold*(np.max(input[0].data[0,:,:],axis=(0,1))-mean)
        imgs_bgremoved=input[0].data-mean-bg_threshold
        imgs_bgremoved[imgs_bgremoved<0.]=0.
        total = np.sum(imgs_bgremoved)
        indices = np.ogrid[[slice(0, i) for i in imgs_bgremoved.shape]]
        print(range(imgs_bgremoved.ndim))
        print(imgs_bgremoved.shape)
        
        for axis in range(imgs_bgremoved.ndim):
            check=np.sum(indices[axis] * imgs_bgremoved)
            print(check)
        return np.array([np.sum(indices[axis] * data) / total / oversampling[axis] for axis in range(data.ndim)])[::-1]

        cl= photutils.centroid_com (imgs_bgremoved[4,:,:])
        print(cl)
        print(total)
        with Pool(processes=4) as p:
            cl=p.map(photutils.centroid_com,imgs_bgremoved)
            print("test1")
            hfdl=p.map(get_hfd,zip(cl,imgs))
            print("test2")
            c=np.vstack(cl)
            print("test3")
            hfd=np.vstack(hfdl)
            print("test4")
            removeconst=True
            if removeconst:
                c=c-c.mean(0)
    return np.hstack((c,hfd))
    print(C)

#""""
#""""
cube = np.zeros((50,1000,1000)) #Here 1000x1000 is the dimension of the individual fits images and 50 is the third perpendicular axis(time/freq)

for i in range(50):
    hdu = fits.open('image' + str(i) + '.fits') #The fits images that you want to combine have the name string 'image' + str(i) + '.fits'
    data = hud[0].data[:,:]
    cube[i,:,:] = data

hdu_new = fits.PrimaryHDU(cube)
hdu_new.writeto('cube.fits')


#""""
#""""

    mean,median,std = stats.sigma_clipped_stats(imgs[0,:,:],
                                                sigma=sigma,
                                                maxiters=2,
                                                cenfunc='median')   
    C=centr.get_centroids(Img,removeconst=False)

test_stack()