import numpy as np
from plank_phantom import phantom_plank
import line_geometry as lg
import numpy as np
from flexdata import display
from flexdata import data
from flextomo import projector
import matplotlib.pyplot as plt

variable = 'angles'
ringwidths = np.array([1.0])

angles = np.array([0])
save_path = 'test/'
sod = 200 #in mm
odd = 400 # in mm

bb = 2 #detector binning
det_pixel = 0.1*bb
det_width = np.int(np.ceil(1944/bb)) #pixels
det_height = np.int(np.ceil(1536/bb))

pix_size = 0.05
vox_size = 0.05

sirt_iter = 50

phantom_size = (30,30,30)

angle = 0 
angle = np.deg2rad(angle)

# Below is unnecessary
# source_range = lg.safe_range(phantom_size,angle, sod)
# det_range = source_range
# print(source_range)

# #create forward geometry
# geom = lg.line_geometry(sod, odd, det_pixel, pix_size, source_range, det_range, plot = False)
# n_proj = int(np.ceil(lg.system_details(geom, phantom_size, det_width)))*2

blur = 10

for j, ring_width in enumerate(ringwidths):
    print(f"j: {j}, Ring Width: {ring_width}")
    for i in angles: #change this line! 
        name = f'phantom_width{ring_width}_size({phantom_size[0]},{phantom_size[1]},{phantom_size[2]})_angle{angle}_blur{blur}'

        #create phantom with tree ring size
        """
        - Phantom size: A triple of (thickness, length, width)
        - angle: Angle at which the image 
        - p:
        - ring_width: 
        - y1, y2: Have been set to minumum and maximum attenuation coefficients instead of density values
        - gaussian_blur: to be adjusted as necessary - Not really sure how to adjust this
        """
        
        P = phantom_plank(phantom_size, angle = np.deg2rad(i), p = pix_size, ring_width = ring_width, gaussian_blurr=blur).transpose([0,2,1]) # Not sure why this is here. 
        print(f"Shape of Phantom data: {P.shape}\n(in cm):")
        image = P[:,0,:]
        plt.imsave(save_path + name+'.png', image, vmin = -1, vmax =2, cmap = 'gray')
        display.slice(P, title = 'Phantom', dim = 1, index = 0)
        print("Finished saving phantom")

        exit()
    
        #Do a forward projection
        print("Beginning forward projection")
        proj = np.zeros([det_height, n_proj, det_width], dtype = 'float32') #dim 1 is number of projections
        projector.forwardproject(proj, P, geom)
        display.slice(proj, dim = 1)
        proj_image = proj[:,proj.shape[1]//2,:]
        plt.imsave(save_path+'projection.png', proj_image, cmap = 'gray')
        print("Finished forward projection")
        

        #Define reconstruction volume and calculate which slice to save for measurement. 
        P_n = (int(np.ceil(phantom_size[0]*1.5/vox_size)), int(np.ceil(phantom_size[1]*1.2/vox_size)), int(np.ceil(phantom_size[2]*1.5/vox_size)))
        slice_front = round(P_n[1]/2-phantom_size[1]/vox_size/2)
        print('slice front object', slice_front)
        slice_measure = round(P_n[1]/2-(phantom_size[1]/2/vox_size)*0.75)
        print('slice for measurement', slice_measure)
        
        #Create reconstruction geometry and reconstruct
        geom_recon = lg.line_geometry(sod, odd, det_pixel, vox_size, source_range, det_range, plot = False)
        geom_recon['src_vrt_rng'] = geom['src_vrt_rng']
        projector.subsets = 1

        vol_rec = np.ascontiguousarray(np.zeros(P_n).astype('float32'))
        
        #SIRT reconstruction
        projector.SIRT(proj, vol_rec, geom_recon, iterations = sirt_iter)
    
        display.slice(vol_rec, index = slice_measure, title = 'SIRT', dim = 1)
        
        crop = (P_n[0] - 1/1.5*P_n[0],P_n[2]-1/1.5*P_n[2])

        #save image
        image = vol_rec[:,slice_measure,:][int(1/2*crop[0]):int(-1/2*crop[0]),int(1/2*crop[1]):int(-1/2*crop[1])]
        name2 = f'recon_width{j+1}'+variable + '%d'%i
        plt.imsave(save_path + name2+'.png', image, vmin = -1, vmax =2, cmap = 'gray')
    
