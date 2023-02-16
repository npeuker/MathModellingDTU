"""
Credit to: @mikeboers

NOTES:
"PyAV is a Pythonic binding for FFmpeg" (https://mikeboers.github.io/PyAV/).
This script was tested with a 1920x1080 video. Crop and resize sizes should be changed in the method below as per 
your requirements.
"""

import av
import PIL
import skimage.io
from skimage.transform import resize, pyramid_reduce

import numpy as np
import os

video_name=input("Enter the name of the video file: ")



def video_frames_writer(video_dir, video_name, writer_type, crop_and_resize_image):
    """
    Writes a (height, width, 3) shaped image in a subdirectory named after the video's name in the video_dir.
    :param video_dir: directory where the video is located
    :param video_name: .avi video file name
    :param writer_type: package used for writing the frames onto disk; 0: PIL; 1: skimage
    :param crop_and_resize_image: boolean flag
    :return: None
    """

    save_dir = video_dir + video_name.split('.')[0]
    os.makedirs(os.path.join('.', save_dir), exist_ok=True)

    container = av.open(video_dir + video_name)
    for frame in container.decode(video=0):
        if frame.index % 100 == 0:
            print("processed frame index {}".format(frame.index))

        img_pil = frame.to_image()
        width, height = img_pil.size  # width, height for this read PIL image

        if writer_type == 0:
            if crop_and_resize_image:
                # 0 crop and resize using PIL
                img_pil_cropped = img_pil.crop((240, 0, width - 240, height))  # (x0, y0, x1, y1)
                resize_width = 320
                ratio = resize_width / float(img_pil_cropped.size[0])
                resize_height = int(float(img_pil_cropped.size[1]) * float(ratio))
                img_pil_down = img_pil_cropped.resize((resize_width, resize_height), PIL.Image.ANTIALIAS)
                img_pil_down.save(os.path.join(save_dir, video_name.split('.')[0]) + '_frame_%05d.jpg' % frame.index)
            else:
                img_pil.save(os.path.join(save_dir, video_name.split('.')[0]) + '_frame_%05d.jpg' % frame.index)

        elif writer_type == 1:
            img_arr = np.asarray(img_pil)  # converting PIL (<class 'PIL.Image.Image'>) to (<class 'numpy.ndarray'>)
            h, w, c = img_arr.shape  # h, w, c for skimage
            # this is exact same as when you read a .jpg image using skimage.io.imread (h, w, c)

            if crop_and_resize_image:
                # 1 crop and resize using skimage.io
                img_sk_cropped = img_arr[0:h, 240:w-240]  # x0:x1,y0:y1
                img_sk_down = pyramid_reduce(img_sk_cropped, downscale=4.5)
                skimage.io.imsave(os.path.join(save_dir, video_name.split('.')[0]) + '_frame_%05d.jpg' % frame.index,
                                  img_sk_down)
            else:
                skimage.io.imsave(os.path.join(save_dir, video_name.split('.')[0]) + '_frame_%05d.jpg' % frame.index,
                                  img_arr)

    container.close()
    print("Processed the video {} and wrote individual frames to folder {}".format(video_name, save_dir))


video_frames_writer(video_dir=r'C:/Users/miles/OneDrive/Desktop/Year 3/Math Modelling/Project 1 - Optical Flow/videos/', video_name=video_name, writer_type=0, crop_and_resize_image=False)