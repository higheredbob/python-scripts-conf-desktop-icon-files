#!/usr/bin/env python

import numpy as np
import cv2
import sys

from scipy import misc
from PIL import Image
from skimage import data, draw, transform, util, filters, color
import matplotlib.pyplot as plt


def parse_command(argv):

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img', dest='img', required=True,
                        action='store', default=None, metavar='FILE',
                        help='image to seam-carve')
    parser.add_argument('-r', '--rm_object', dest='rm_object',
                        action='append', default=None, type=list,
                        help='remove an object from an image, list in pairs')
    parser.add_argument('-o', '--opts', dest='opts', action='store',
                        default='pyplot', choices=['pyplot', 'cv2'],
                        help='chose the plotting/visualization library to use')
    parser.add_argument('-d', '--direct', dest='direct', action='store',
                        default='horizontal', choices=['horizontal', 'vertical'],
                        help='direction to cut seam by')
    parser.add_argument('-m', '--magnitude', dest='magnitude', action='store',
                        default=None, type=str, nargs='?', choices=['scharr','sobel','roberts'],
                        help='apply the filter for edge magnitude')

    return parser.parse_args()

def main(argv=None):

    args = parse_command(argv)

    try:
        im = Image.open(args.img)
        w,h = im.size
    except:
        print("error opening %s not an image" %(pix_img))
        exit(1)


    if args.opts == 'cv2' and args.rm_object != None:
        print('error; {} cannot be used in conjunction with {} '.format(args.opts, args.rm_object))
        exit(1)

    if args.opts == 'pyplot' and args.rm_object == None:

        try:
            img = data.imread(args.img)
            img = util.img_as_float(img)
        except:
            print('error reading in img %s' %(args.img))
            exit(1)



        print('{} is {}x{}'.format(args.img, w,h))

        if args.magnitude == 'sobel':
            mag_img = filters.sobel(color.rgb2gray(img))
        if args.magnitude == 'roberts':
            mag_img = filters.scharr(color.rgb2gray(img))
        if args.magnitude == 'scharr':
            mag_img = filters.roberts(color.rgb2gray(img))

        for numseams in range(15, 300, 15):
            out = transform.seam_carve(img, mag_img, args.direct, numseams)

            #plt.figure()
            #plt.imshow(out)
            h,t = str(args.img).split('.')
            misc.imsave('{}seam.{}'.format(h, t), out)



    if args.rm_object != None:
        try:
            img = data.imread(args.img)
            img = util.img_as_float(img)
            nimg = filters.sobel(color.rgb2gray(img))
        except:
            print('error')
            exit(1)

        h1_col = np.array([0,1,0])
        masked_img = img.copy()
        poly = [(664,986), (641,993), (619,971), (609,942), (629,920), (647,909), (658,899), (678,892), (716,902), (728,914), (737,931), (744,959), (727,987), (713,1001), (664,986)]
        pr = np.array([p[0] for p in poly])
        pc = np.array([p[1] for p in poly])
        rr, cc = draw.polygon(pr, pc)
        masked_img[rr, cc, :] = masked_img[rr, cc, :]*0.5 + h1_col*.5
        plt.figure()
        plt.imshow(masked_img)
        nimg[rr, cc] -= 1000
        plt.figure()
        out = transform.seam_carve(img, nimg, args.direct, 80)
        resized = transform.resize(img, out.shape, mode='reflect')
        plt.imshow(out)
        #plt.show()
        h,t = str(args.img).split('.')
        misc.imsave('{}rm.{}'.format(h, t), out)

    if args.opts == 'cv2':
        try:
            imge = data.imread(args.img)
            #imge = cv2.imread(imge)
            gray = cv2.cvtColor(imge, cv2.COLOR_BGR2GRAY)
        except:
            print('error')
            exit(1)

        if args.magnitude == 'sobel':
            mag = filters.sobel(gray.astype('float'))
        if args.magnitude == 'roberts':
            mag = filters.roberts(gray.astype('float'))
        if args.magnitude == 'scharr':
            mag = filters.scharr(gray.astype('float'))

        for numseams in range(10, 70, 10):
            sCarved = transform.seam_carve(imge, mag, args.direct, numseams)
            cv2.imshow('Carved', sCarved)
            cv2.waitKey(0)
            h,t = str(args.img).split('.')
            misc.imsave('{}seamcv.{}'.format(h, t), sCarved)


if __name__ == '__main__':
    main(sys.argv)
