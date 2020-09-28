import cv2
import numpy as np

class ForwardEnergy(object):
    """
    Forward energy algorithm as described in "Improved Seam Carving for Video Retargeting"
    by Rubinstein, Shamir, Avidan.

    Vectorized code adapted from
    https://github.com/axu2/improved-seam-carving
    """

    def __init__(self, arg):
        super(, self).__init__()
        self.arg = arg
    
        h, w = img.shape[:2]
        img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float64)

        energy_map = np.zeros((h,w))
        m = np.zeros((h,w))

        U = np.roll(img, 1, axis = 0)
        L = np.roll(img, 1, axis = 1)
        R = np.roll(img, -1, axis = 1)

        cU = np.abs(R - L)
        cL = np.abs(U - L) + cU
        cR = np.abs(U - R) + cU

        for i in range(1, h):
            mU = m[i-1]
            mL = np.roll(mU, 1)
            mR = np.roll(mU, -1)

            mULR = np.array([mU, mL, mR])
            cULR = np.array([cU[i], cL[i], cR[i]])
            mULR += cULR

            argmins = np.argmin(mULR, axis = 0)
            m[i] = np.choose(argmins, mULR)
            energy_map[i] = np.choose(argmins, cULR)

        #Saves the first energy map calculated (before any seam removed)
        global firstCalculation
        if firstCalculation == True:
            cv2.imwrite(FORWARD_ENERGY_PATH, np.rot90(energy_map, 3, (0, 1)))
            firstCalculation = False

        return energy_map
