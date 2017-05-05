import cv2
#import open cv
import numpy as np
#import numpy for scientific calculations
from matplotlib import pyplot as plt
#display the image
from PIL import Image


green=(0,255,0)
red=(255,0,0)
blue=(0,0,255)


def find_biggest_contour(image):
	image=image.copy()

	_ , contours , hierarchy=cv2.findContours(image,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	contour_sizes=[(cv2.contourArea(contour),contour) for contour in contours]
	biggest_contour=max(contour_sizes,key=lambda x:x[0])[1]
	mask=np.zeros(image.shape,np.uint8)
	cv2.drawContours(mask,[biggest_contour],-1,255,-1)

	return biggest_contour,mask

def overlay_mask(mask,image):
	rgb_mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
	img=cv2.addWeighted(rgb_mask,0.5,image,0.5,0)
	return img


def circle_contour(image,contour):

	image_with_ellipse=image.copy()

	ellipse=cv2.fitEllipse(contour)
	global centros
	global distancias
	global angulo
	centros = ellipse[0]
	distancias = ellipse[1]
	angulo = ellipse[2]
	print("centroX {}".format(ellipse[0][0]))
	print("centroY {}".format(ellipse[0][1]))

	img = cv2.imread("banana.jpg")
	cv2.ellipse(image_with_ellipse,ellipse,red,2,1)

	return image_with_ellipse


def show(image):

	plt.figure(figsize=(10,10))
	plt.imshow(image,interpolation='nearest')

def draw_banana(image):

	#PRE PROCESSING OF IMAGE

	image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

	maxsize=max(image.shape)

	scale=700/maxsize

	image=cv2.resize(image,None,fx=scale,fy=scale)

	image_blur=cv2.GaussianBlur(image,(7,7),0)

	image_blur_hsv=cv2.cvtColor(image_blur,cv2.COLOR_RGB2HSV)

	min_color=np.array([0,92,84])
	#min_color=np.array([0,224,0])
	max_color=np.array([30,256,256])

	mask1=cv2.inRange(image_blur_hsv,min_color,max_color)

	min_color2=np.array([100,150,150])
	max_color2=np.array([70,256,256])

	mask2=cv2.inRange(image_blur_hsv,min_color2,max_color2)

	mask=mask1+mask2

	kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
	#print kernel solo muestra un puunto
	#cambiar los parametros (15,15) solo cambia el grosor de la linea de la elipse
	# cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)).getRadius no esta disponible en cv2


	mask_closed=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

	mask_cleaned=cv2.morphologyEx(mask_closed,cv2.MORPH_OPEN,kernel)

	big_contour,mask_fruit=find_biggest_contour(mask_cleaned)

	overlay=overlay_mask(mask_cleaned,image)
	#print overlay solo mustra el banano sin la elipse

	circled=circle_contour(overlay,big_contour)
	#circled es el banano con un overlay aplicado

	show(circled)

	bgr=cv2.cvtColor(circled,cv2.COLOR_RGB2BGR)

	return bgr


def cortar():
	img = cv2.imread("banana_new.jpg")
	print(centros)
	crop_img = img[ (int(centros[1])-(int(distancias[1]*0.5))):(int(centros[1])+(int(distancias[1]*0.5))), (int(centros[0])-(int(distancias[0]*0.5))):(int(centros[0])+(int(distancias[0]*0.5)))                     ]
	 # Crop from x, y, w, h -> 100, 200, 300, 400
	# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
	cv2.imwrite('cortar.jpg',crop_img)




banana=cv2.imread('banana.jpg')
result_banana=draw_banana(banana)
cv2.imwrite('banana_new.jpg',result_banana)
#imagen girada por el angulo de la primera elipse encontrada
rotImg = Image.open("banana.jpg")
rotImg2 = rotImg.rotate(angulo)
rotImg2.save("img2.jpg")
#se crea la segunda ellipse rotada 0 en su angulo
bananaRotada=cv2.imread('img2.jpg')
result_banana=draw_banana(bananaRotada)
cv2.imwrite('banana_new.jpg',result_banana)
cortar()