!wget http://images.cocodataset.org/zips/train2017.zip
!unzip 'train2017.zip' -d 'train2017'

!wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
!unzip 'annotations_trainval2017.zip' -d 'annotations_trainval2017'


from pycocotools.coco import COCO
import numpy as np
import skimage.io as io

import matplotlib.pyplot as plt
import pylab
#pylab.rcParams['figure.figsize'] = (8.0, 10.0)
import requests

annFile = '/content/annotations_trainval2017/annotations/instances_train2017.json'

coco=COCO(annFile)

cats = coco.loadCats(coco.getCatIds())
catIds = coco.getCatIds(catNms=['bicycle', 'person'])
imgIds = coco.getImgIds(catIds=catIds)
images = coco.loadImgs(imgIds)


img_array = []
imgid_array = []
imgdim_array = []
for i in range(len(images)):
  img_array.append(images[i]['file_name'])
  imgid_array.append(images[i]['id'])
  imgdim_array.append([images[i]['width'], images[i]['height']])




annIds = coco.getAnnIds(imgIds=imgid_array)
anns = coco.loadAnns(annIds)

bbox_array = []
for i in imgid_array:
  bbox_img = []
  for j in anns:
    if j['image_id']==i and (j['category_id'] == 1 or j['category_id'] == 2):
      j['bbox'].append(j['category_id'])
      bbox_img.append(j['bbox'])

  bbox_array.append(bbox_img)

print(len(img_array))

imagenum = 11

print(bbox_array[imagenum])
I = io.imread('/content/train2017/train2017/' + img_array[imagenum])
plt.imshow(I)


def format_bbox(dim_array, bboxarr):
  #Eksempel bboxarr [[11.2, 379.15, 269.01, 179.73, 2], [79.66, 275.68, 127.68, 266.99, 1]]
  #Eksempel dim_array [420, 630]
  c=-1
  bbox_form_arr = []
  for i in dim_array:
    c+=1
    size = max(i)
    grid_size = size/7
    landscape = False
    padding = abs(i[0]-i[1])/2
    if i[0]>i[1]:
      landscape = True
    
    j=bboxarr[c]
    bbox_for_img=[]
    for k in j:

      if landscape:
        x_grid = ((k[0]+(k[2]/2))//grid_size)
        y_grid = (((k[1]+(k[3]/2))+padding)//grid_size)
        x_pos = ((k[0]+(k[2]/2))%grid_size)/grid_size
        y_pos = (((k[1]+(k[3]/2))+padding)%grid_size)/grid_size
      else:
        x_grid = (((k[0]+(k[2]/2))+padding)//grid_size)
        y_grid = ((k[1]+(k[3]/2))//grid_size)
        x_pos = (((k[0]+(k[2]/2))+padding)%grid_size)/grid_size
        y_pos = ((k[1]+(k[3]/2))%grid_size)/grid_size

      bbox_formatted = [x_grid, y_grid, x_pos, y_pos, k[2]/size, k[3]/size, k[4]]
      bbox_for_img.append(bbox_formatted)
    bbox_form_arr.append(bbox_for_img)
  return bbox_form_arr

bboxarray = format_bbox(imgdim_array, bbox_array)
print(bboxarray[0])




def bbox_to_matrix(bbox):
  reftensor = np.zeros((7,7,5)).tolist()
  for i in bbox:
    coordx = int(i[0])
    coordy = int(i[1])

    reftensor[coordx][coordy]=i[2:]

  return reftensor


def list_bboxmat(bboxlist):
  bbox_list = []
  for i in bboxlist:
    bbox_list.append(bbox_to_matrix(i))
  return np.asarray(bbox_list)

bboxarray2 = list_bboxmat(bboxarray)



from skimage.transform import resize

def format_img(img):

  size = max(img.shape)
  background = np.zeros((size,size,3))

  if img.shape[0]<img.shape[1]:
    offset = np.array((int(abs(img.shape[0]-img.shape[1])/2),0))
  else:
    offset = np.array((0, int(abs(img.shape[0]-img.shape[1])/2)))

  background[offset[0]:offset[0]+img.shape[0],offset[1]:offset[1]+img.shape[1]] = img
  
  bottle_resized = resize(background/255, (448, 448))
  return bottle_resized


imgarr = []
for i in range(300):
  
  I = io.imread('/content/train2017/train2017/' + img_array[i])
  if len(I.shape)!=2:
    imgarr.append(format_img(I))
  
imgarr = np.asarray(imgarr)
print("done")




with open('/content/bboxarr.npy', 'wb') as f:
    np.save(f, bboxarray2)
with open('/content/imgarr.npy', 'wb') as f:
    np.save(f, imgarr)


plt.imshow(imgarr[num])
