    boxes = interpreter.get_tensor(output_details[0]['index'])[0] 
    classes = interpreter.get_tensor(output_details[1]['index'])[0] 
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    #num = interpreter.get_tensor(output_details[3]['index'])[0]
    





    pos_object1_mult = []
    pos_object2_mult = []


    for i in range(len(classes)):
        if scores[i]>0.5:
            if classes[i]==0:
                pos_object1 = [boxes[i][0], boxes[i][1]]
                pos_object1_mult.append(pos_object1)
            elif classes[i]==1:
                pos_object2 = [boxes[i][0], boxes[i][1]]
                pos_object2_mult.append(pos_object2)
    try:
        for i in pos_object1_mult:
            index_and_dist = []
            for j in pos_object1_mult2:
                dist = (((i[0]-j[0])**2)+((i[1]-j[1])**2))**0.5
                if len(index_and_dist)==0:
                    index_and_dist = [pos_object1_mult2.index(j), dist]
                elif index_and_dist[1]>dist:
                    index_and_dist = [pos_object1_mult2.index(j), dist]

            if len(pos_object1_mult)>0 and len(pos_object1_mult2)>0:
                if len(pos_object1_mult)==len(pos_object1_mult2):

                    if i[1]>0.5 and pos_object1_mult2[index_and_dist[0]][1]<0.5:
                        print("fotgjenger mot høyre")
                    if i[1]<0.5 and pos_object1_mult2[index_and_dist[0]][1]>0.5:
                        print("fotgjenger mot venstre")


        for i in pos_object2_mult:
            index_and_dist2 = []
            for j in pos_object2_mult2:
                dist2 = (((i[0]-j[0])**2)+((i[1]-j[1])**2))**0.5
                if len(index_and_dist2)==0:
                    index_and_dist2 = [pos_object2_mult2.index(j), dist2]
                elif index_and_dist2[1]>dist2:
                    index_and_dist2 = [pos_object2_mult2.index(j), dist2]

            if len(pos_object1_mult)>0 and len(pos_object1_mult2)>0:
                if len(pos_object2_mult)==len(pos_object2_mult2):
                    if i[1]>0.5 and pos_object2_mult2[index_and_dist2[0]][1]<0.5:
                        print("syklist mot høyre")
                    if i[1]<0.5 and pos_object2_mult2[index_and_dist2[0]][1]>0.5:
                        print("syklist mot venstre")
        for i in pos_object2_mult:
            index_and_dist2 = []
            for j in pos_object2_mult2:
                dist2 = (((i[0]-j[0])**2)+((i[1]-j[1])**2))**0.5
                if len(index_and_dist2)==0:
                    index_and_dist2 = [pos_object2_mult2.index(j), dist2]
                elif index_and_dist2[1]>dist2:
                    index_and_dist2 = [pos_object2_mult2.index(j), dist2]

            if len(pos_object1_mult)>0 and len(pos_object1_mult2)>0:
                if len(pos_object2_mult)==len(pos_object2_mult2):
                    if i[1]>0.5 and pos_object2_mult2[index_and_dist2[0]][1]<0.5:
                        print("syklist mot høyre")
                    if i[1]<0.5 and pos_object2_mult2[index_and_dist2[0]][1]>0.5:
                        print("syklist mot venstre")

    except NameError:
        print("No previous detection")
    

    




    pos_object2_mult2 = pos_object2_mult
    pos_object1_mult2 = pos_object1_mult

