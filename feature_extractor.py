import numpy as np
from collections import deque

def calculate_angle(a,b,c):
    a,b,c=np.array(a),np.array(b),np.array(c)
    ang=np.abs(np.arctan2(c[1]-b[1],c[0]-b[0]) -
               np.arctan2(a[1]-b[1],a[0]-b[0]))*180/np.pi
    return 360-ang if ang>180 else ang


class FeatureExtractor:
    def __init__(self):
        self.hip_history = deque(maxlen=5)
        self.prev_coords = None

    def extract(self,lm):

        ls,rs=lm[11],lm[12]
        cx,cy=(ls.x+rs.x)/2,(ls.y+rs.y)/2
        scale=((ls.x-rs.x)**2+(ls.y-rs.y)**2)**0.5 or 1

        coords=[]
        raw_xy=[]

        for p in lm:
            nx=(p.x-cx)/scale
            ny=(p.y-cy)/scale
            coords.extend([nx,ny,p.z])
            raw_xy.append([nx,ny])

        coords=np.array(coords)
        raw_xy=np.array(raw_xy)

        def pt(i): return [lm[i].x,lm[i].y]

        angles=np.array([
            calculate_angle(pt(11),pt(13),pt(15)),
            calculate_angle(pt(12),pt(14),pt(16)),
            calculate_angle(pt(23),pt(25),pt(27)),
            calculate_angle(pt(24),pt(26),pt(28)),
            calculate_angle(pt(11),pt(23),pt(25)),
            calculate_angle(pt(12),pt(24),pt(26)),
            calculate_angle(pt(13),pt(11),pt(23)),
            calculate_angle(pt(14),pt(12),pt(24))
        ]) / 180.0

        # Motion
        hip_y=(lm[23].y+lm[24].y)/2
        hip_norm=(hip_y-cy)/scale

        self.hip_history.append(hip_norm)
        hip_vel = 0 if len(self.hip_history)<2 else (self.hip_history[-1]-self.hip_history[-2])

        # Full-body motion energy
        if self.prev_coords is None:
            motion_energy=0
        else:
            motion_energy=np.mean(np.linalg.norm(raw_xy-self.prev_coords,axis=1))

        self.prev_coords = raw_xy.copy()

        # Knee features
        knee_left=angles[2]
        knee_right=angles[3]
        knee_mean=(knee_left+knee_right)/2
        knee_diff=abs(knee_left-knee_right)

        # Torso
        shoulder_mid=[(lm[11].x+lm[12].x)/2,(lm[11].y+lm[12].y)/2]
        hip_mid=[(lm[23].x+lm[24].x)/2,(lm[23].y+lm[24].y)/2]

        torso_angle=calculate_angle(
            [shoulder_mid[0], shoulder_mid[1]-0.1],
            shoulder_mid,
            hip_mid
        )/180.0

        features=np.concatenate([
            coords,
            angles,
            [hip_norm, hip_vel, knee_mean, knee_diff, motion_energy, torso_angle]
        ])

        return features, motion_energy, angles