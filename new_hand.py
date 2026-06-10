import mediapipe as mp
import cv2

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

hand=mp_hands.Hands()

video=cv2.VideoCapture(0)
while True:
    suc,img=video.read()
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hand.process(img1)
    tipid=[4,8,12,16,20]
    lmlst=[]
    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            for id,lm in enumerate(handlm.landmark):
                #print(id,lm)
                lmlst.append([id,lm.x,lm.y])
            if len(lmlst)==21:
                fingerlst=[]
                count=0
                #THUMB
                if lmlst[8][1]<lmlst[20][1]:
                    if lmlst[4][1]>lmlst[3][1]:
                        fingerlst.append(0)
                    else:
                        fingerlst.append(1)
                else:
                    if lmlst[4][1]<lmlst[3][1]:
                        fingerlst.append(0)
                    else:
                        fingerlst.append(1)

                for i in range (1,5):
                    if lmlst[tipid[i]][2]>lmlst[tipid[i]-2][2]:
                        fingerlst.append(0)
                    else:
                        fingerlst.append(1)
                
                count=sum(fingerlst)
                cv2.putText(img,str(count),org=(70,70),fontFace=cv2.FONT_HERSHEY_COMPLEX,fontScale=3,color=(0,0,255),thickness=4)

            mp_drawing.draw_landmarks(img,handlm,mp_hands.HAND_CONNECTIONS)
        
    cv2.imshow('webcam',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break

video.release()
cv2.destroyAllWindows()