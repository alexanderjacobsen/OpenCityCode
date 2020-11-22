def IoU(cell, vec1, vec2):
  x1=(cell[0]+(1/7)*vec1[0])-vec1[2]*0.5
  y1=(cell[1]+(1/7)*vec1[1])-vec1[3]*0.5

  x2=(cell[0]+(1/7)*vec1[0])+vec1[2]*0.5
  y2=(cell[1]+(1/7)*vec1[1])+vec1[3]*0.5

  x3=(cell[0]+(1/7)*vec2[0])-vec2[2]*0.5
  y3=(cell[1]+(1/7)*vec2[1])-vec2[3]*0.5

  x4=(cell[0]+(1/7)*vec2[0])+vec2[2]*0.5
  y4=(cell[1]+(1/7)*vec2[1])+vec2[3]*0.5

  l = abs(max(x1, x3)-min(x2, x4))
  h = abs(max(y1, y3)-min(y2, y4))
  intersection = l*h
  a1 = vec1[2]*vec1[3]
  a2 = vec2[2]*vec2[3]
  return intersection/((a1+a2)-intersection)

#print(IoU([6,6], [0.6, 0, 1, 1], [1, 0.9, 1/7, 1/7]))


def loss_per_pred(truth, pred):
  #Eksempel pred [SxS][1, 0.3, 0.4, 0.5, 0.5, 1, 0.3, 0.4, 0.5, 0.5, 0 , 0, 0, 1, 0, 0]
  #Eksempel truth [[1.0, 5.0, 0.6013437500000001, 0.8274296875, 0.16893750000000002, 0.27345312499999996, 2], [3.0, 4.0, 0.6807265625, 0.4748437499999998, 0.765921875, 0.65821875, 1]]
  with_obj = []

  coord_error = 0
  size_error = 0
  conf_error = 0
  class_error = 0
  conf_error2 = 0
  conf_error_noobj = 0
  
  truth_vec = []

  c1=-1
  for i in truth:
    c1+=1
    c2=-1
    for j in i:
      c2+=1
      if j[-1] != 0:
        bbox_ins = [c1, c2, j[0], j[1], j[2], j[3], j[4]]
        truth_vec.append(bbox_ins)
    

  for bbox in truth_vec:
    grid_cell = bbox[:2]
    with_obj.append(grid_cell)
    predcell = pred[grid_cell[0]][grid_cell[1]]

    pred1 = predcell[:5]
    pred2 = predcell[5:10]
    predclass = predcell[10:]

    IoU1 = IoU(grid_cell, pred1[1:], bbox[2:-1])
    IoU2 = IoU(grid_cell, pred2[1:], bbox[2:-1])

    if IoU1>=IoU2:
      highestIoU = pred1
      highestIoUVal = IoU1
      lowestIoU = pred2
    else:
      highestIoU = pred2
      highestIoUVal = IoU2
      lowestIoU = pred1
    
    coord_error += ((highestIoU[1]-bbox[2])**2)+((highestIoU[2]-bbox[3])**2)
    size_error += (((highestIoU[3]**0.5)-(bbox[4]**0.5))**2)+(((highestIoU[4]**0.5)-(bbox[5])**0.5)**2)
    conf_error += (highestIoU[0]-highestIoU)**2

    if bbox[-1] == 1:
      one_hot = np.array([1,0])
    else:
      one_hot = np.array([0,1])

    class_error += ((predclass[0]-one_hot[0])**2)+((predclass[1]-one_hot[1])**2)
    conf_error2 += ((lowestIoU[0]-highestIoU)**2)
  
  
  length = -1
  for i in pred:
    length+=1
    width = -1
    for j in i:
      width+=1
      if not ([width, height] in with_obj):
        conf_error_noobj += (j[0])**2
  total_loss = 5*coord_error + 5*size_error + conf_error + class_error + 0.5*conf_error2 + 0.5*conf_error_noobj
  return total_loss



def tot_loss(truth, pred):
  n=-1
  loss_array = np.array([])
  for i in pred:
    n+=1
    loss_array = np.append(loss_array, loss_per_pred(truth[n], i))
  return loss_array
  
  
  
  
  
  import tensorflow as tf
from tensorflow.keras import datasets, Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Reshape

x_train = imgarr
y_train = bboxarray2

model = Sequential()

model.add(Conv2D(16, (3,3), activation="relu"))
model.add(MaxPooling2D((2,2), 2))


model.add(Conv2D(32, (3,3), activation="relu"))
model.add(MaxPooling2D((2,2), 2))


model.add(Conv2D(64, (3,3), activation="relu"))
model.add(MaxPooling2D((2,2), 2))

model.add(Conv2D(128, (3,3), activation="relu"))
model.add(MaxPooling2D((2,2), 2))


model.add(Conv2D(256, (3,3), activation="relu"))
model.add(MaxPooling2D((2,2), 2))

model.add(Conv2D(512, (3,3), activation="relu"))
model.add(MaxPooling2D((2,2), 2))

model.add(Conv2D(1024, (3,3), activation="relu"))
model.add(Conv2D(1024, (3,3), activation="relu"))
model.add(Conv2D(1024, (3,3), activation="relu"))



model.add(Flatten())
model.add(Dense(100, activation="relu"))
model.add(Dense(588, activation="softmax"))

model.add(Reshape((7,7,12)))



model.compile(loss=tot_loss, optimizer="adam", metrics=["accuracy"])


model.fit(x_train, y_train, batch_size=10, epochs=15)
print(model.summary())
