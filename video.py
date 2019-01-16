import cv2,time,pandas
import datetime
first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])
video=cv2.VideoCapture(0)
#a=0
while True:
    #a=a+1
    check,frame=video.read()
    status=0
    #print(check)
    #print(frame)

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None:
        first_frame=gray
        continue


    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)


    (_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contours in cnts:
        if cv2.contourArea(contours)<10000:
            continue
        status=1;
        (x,y,w,h)=cv2.boundingRect(contours)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    status_list.append(status)
    status_list=status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.datetime.now())

    cv2.imshow("Gray frame",frame)
    cv2.imshow("Delta frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("color Frame",frame)

    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            times.append(datetime.datetime.now())
        break
#print(a)
print(status_list)
print(times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[1],"End":times[i+1]},ignore_index=True)
df.to_csv("Times.csv")
#print(gray)
#print(delta_frame)
video.release()
cv2.destroyAllWindows