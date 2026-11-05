import cv2

IMPORTANT=[11,12,13,14,15,16,23,24,25,26,27,28]

CONNECTIONS=[
    (11,13),(13,15),(12,14),(14,16),
    (11,12),(11,23),(12,24),(23,24),
    (23,25),(25,27),(24,26),(26,28)
]

def draw_pose(frame,lm,angles=None):
    h,w,_=frame.shape

    for a,b in CONNECTIONS:
        x1,y1=int(lm[a].x*w),int(lm[a].y*h)
        x2,y2=int(lm[b].x*w),int(lm[b].y*h)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),3)

    for i in IMPORTANT:
        x,y=int(lm[i].x*w),int(lm[i].y*h)
        cv2.circle(frame,(x,y),5,(255,0,0),-1)

    if angles is not None:
        xk,yk=int(lm[25].x*w),int(lm[25].y*h)
        cv2.putText(frame,f"{int(angles[2]*180)}°",(xk,yk-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)

    return frame