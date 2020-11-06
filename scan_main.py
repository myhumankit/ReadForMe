#!/bin/python3
#coding: utf-8
# python scan_main.py --image images/page.jpg 

# importation bibliotheques python necessaires

import os
import time
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2

# définition des arguments et du passage des arguments

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
    help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# Chargement image, clonage et redimensionnement image selon ration

image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

# Convertion image en niveau de gris et recherche des angles de la page dans l'image

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# option : affiche respectivement dans une fenêtre
# l'image originale et l'image avec les angles détectés

print "STEP 1: Détection des angles"
#cv2.imshow("Image", image)
#cv2.imshow("Edged", edged)
#cv2.waitKey(0)
cv2.destroyAllWindows()

# cherche les contours de l'image avec les angles détectés et conserve
# les plus larges, initialisation de l'apparence.

(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# 
for c in cnts:
    # approximation des contours
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if l'appoximation des contours possède 4 angles
    # nous considérons avoir trouvé l'apparence de la page à lire
    if len(approx) == 4:
        screenCnt = approx
        break

# visualisation de la page à lire  (outline)

print "STEP 2: Recherche les contours d la page à lire"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
#cv2.waitKey(0)
cv2.destroyAllWindows()

# application du script :  four point transform
# visualisation de la page originale
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convertion de l'image traitée en niveau de gris
# 
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255

# affichage de l'image originale et de la page finale à lire
print "STEP 3: Redressement de l'image"
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#cv2.waitKey(0)
#cv2.imwrite("ouyput.png", warped)
#print "Image sauvegardée"

up_file="./images/img.png"
cv2.imwrite(up_file, warped)
time.sleep(5)
#cmd_mov="mv "
#cmd_mov+=up_file
#cmd_mov+=" /home/pi/document-scanner/images/"
#os.system(cmd_mov)
#time.sleep(5)

#cmd_ret="cd ~"
#os.system(cmd_ret)
#time.sleep(5)

os.system("echo job terminé")

#tout les scripts doivent être dans le dossiers /home/pi/document-scanner
