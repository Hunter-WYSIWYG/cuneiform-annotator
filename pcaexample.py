import pandas as pd
import matplotlib
import numpy as np
import os
from math import sqrt

from plyfile import PlyData

from sklearn.decomposition import PCA
from sklearn.datasets import make_classification

input_folder = r"F:\i3mainz_Hochschule Mainz\Keilschriften\neue_orientierung\Neuer Ordner"
# meshnames=["H.T._07-31-102_Pulverdruckverfahren_3_Zusammen_mitPuder_mehrPunkte.ply","H.T._07-31-102_SLA_3_Zusammen_mitPuder_mehrPunkte.ply","H.T_07-31-102_FDM_3_Zusammen_mitPuder_mehrPunkte _keine_Nachverarbeitung_mitLoecher.ply", "HT_07-31-47_3D.ply"]

reduce_factors=[1]

reduce_factor = 1

scaling = False

resultfile=input_folder + "/" + "pca_result.txt"

def rigid_transform_3D(A, B, scale):
    assert len(A) == len(B)
    N = A.shape[0];  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    # print(centroid_A)
    # print(centroid_B)

    # center the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))
    # print(AA)
    # print(BB)
    # print(np.transpose(BB))

    # dot is matrix multiplication for array
    if scale:
        H = np.dot(np.transpose(BB),AA)/ N
    else:
        H = np.dot(np.transpose(BB),AA)

    U, S, Vt = np.linalg.svd(H)
    R = Vt.T * U.T

    # special reflection case
    if np.linalg.det(R) < 0:
        print("Reflection detected")
        Vt[2, :] *= -1
        R = Vt.T * U.T
    if scale:
        varA = np.var(A, axis=0).sum()
        c = 1 / (1 / varA * np.sum(S))  # scale factor
        t = -R * (centroid_B.T * c) + centroid_A.T
    else:
        c = 1
        t = -R * centroid_B.T + centroid_A.T

    # print(R)
    # print(t)
    # print(c)
    return c, R, t

def pcaToWKT(pca):
    wktString+="CS[\"cartesian\",3],"
    """    
    COORDINATEOPERATION["Object To PCA",
  SOURCECRS[CS["cartesian", 3],
    AXIS["X", "geocentricX", ORDER[1],
        LENGTHUNIT["millimetre",1],
        ANGLEUNIT["degree", 0.0174532925199433]
    ],
    AXIS["Y", "geocentricY", ORDER[2],
        LENGTHUNIT["millimetre",1],
        ANGLEUNIT["degree", 0.0174532925199433]
    ],
    AXIS["Z", "geocentricZ", ORDER[3],
        LENGTHUNIT["millimetre",1]
    ]],
  TARGETCRS[CS["cartesian", 3],
    AXIS["X", "geocentricX", ORDER[1],
        LENGTHUNIT["millimetre",1],
        ANGLEUNIT["degree", 0.0174532925199433]
    ],
    AXIS["Y", "geocentricY", ORDER[2],
        LENGTHUNIT["millimetre",1],
        ANGLEUNIT["degree", 0.0174532925199433]
    ],
    AXIS["Z", "geocentricZ", ORDER[3],
        LENGTHUNIT["millimetre",1]
    ]],
  METHOD["Geocentric translations", ID["EPSG", 1031]],
  PARAMETER["X-axis translation", -128.5, LENGTHUNIT["metre", 1]],
  PARAMETER["Y-axis translation",  -53.0, LENGTHUNIT["metre", 1]],
  PARAMETER["Z-axis translation",  153.4, LENGTHUNIT["metre", 1]]
  OPERATIONACCURACY[5],
  AREA["Object extent"],
  BBOX[-43.7, 112.85, -9.87, 153.68]]
  """    

def do_PCA(mesh): 
  pca = PCA()
  pca.fit(mesh)
  PCA(copy=True, n_components=3, whiten=False)
#   print("Fake Annotation: [ 1 1 1 ]")
  f.write("\n") 
  f.write("Vector, Mesh "+meshname+"\n")
  counter=1
  resultmatrix=[0,1,2,3]
  for variance, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(variance)
    f.write("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(np.linalg.norm(pca.mean_-(pca.mean_+v)))+"\n")
    resultmatrix[0]=pca.mean_
    resultmatrix[counter]=pca.mean_+v
    counter+=1
#   print(resultmatrix)
#   print("Fake Annotation Translated: [ "+str(1+pca.mean_[0])+" "+str(1+pca.mean_[1])+" "+str(1+pca.mean_[2])+" ]")
#   print("Fake Annotation Translated: [ "+str(1+pca.mean_[0])+" "+str(1+pca.mean_[1])+" "+str(1+pca.mean_[2])+" ]")
  reducedMesh = pca.transform(mesh)
  return [reducedMesh,pca,resultmatrix]

f = open(resultfile, 'w')  
for root, dirs, files in os.walk (input_folder):
    for meshname in files:
        if os.path.splitext(meshname)[-1]==".ply":
            print("Processing "+str(meshname))
            plyfile = PlyData.read(root + "/" + meshname)
            mesh = pd.DataFrame({
            'x':plyfile['vertex']['x'][::reduce_factor],
            'y':plyfile['vertex']['y'][::reduce_factor],
            'z':plyfile['vertex']['z'][::reduce_factor]
            })
            pca = do_PCA(mesh)
          
            # Objektkoordinaten
            p0_pca_A = pca[2][0]
            p1_pca_A = pca[2][1]
            p2_pca_A = pca[2][2]
            p3_pca_A = pca[2][3]
            # pca-Koordinaten
            p0_pca_B= np.array([0,0,0])
            p1_pca_B= np.subtract(p1_pca_A, p0_pca_A)
            p2_pca_B= np.subtract(p2_pca_A, p0_pca_A)
            p3_pca_B= np.subtract(p3_pca_A, p0_pca_A)
            # Matrizen
            A = np.matrix([p0_pca_A , p1_pca_A, p2_pca_A, p3_pca_A])
            B = np.matrix([p0_pca_B , p1_pca_B, p2_pca_B, p3_pca_B])

            f.write("Matrix A" +"\n")
            f.write(str(A)+"\n")
            f.write("Matrix B" +"\n")
            f.write(str(B)+"\n")

            print ("Matix A")
            print (A)
            print("")
            print ("Matix B")
            print (B)
            print("")

            s, ret_R, ret_t=rigid_transform_3D(A, B,False)

            
            n = B.shape[0]  	    

            ## Find the error
            B2 = (ret_R * B.T) + np.tile(ret_t, (1, n))
            B2 = B2.T
            err = A - B2
            err = np.multiply(err, err)
            err = np.sum(err)
            rmse = sqrt(err / n);

            ##convert to 4x4 transform
            match_target = np.zeros((4,4))
            match_target[:3,:3] = ret_R
            match_target[0,3] = ret_t[0]
            match_target[1,3] = ret_t[1]
            match_target[2,3] = ret_t[2]
            match_target[3,3] = 1

            # print "Points A"
            # print A
            # print ""

            # print "Points B"
            # print B
            # print ""

            # print "Rotation"
            # print ret_R
            # print ""

            # print "Translation"
            # print ret_t
            # print ""

            # print "Scale"
            # print s
            # print ""



            f.write("Rotation" +"\n")
            f.write(str(ret_R)+"\n")
            f.write("Translation" +"\n")
            f.write(str(ret_t)+"\n")
            f.write("Scale" +"\n")
            f.write(str(s)+"\n")
            f.write("RMSE" +"\n")
            f.write(str(rmse)+"\n")

            print("Rotation")
            print(ret_R)
            print("")

            print("Translation") 
            print(ret_t)
            print("")

            print("Scale")
            print(s)
            print("")

            print ("Homogeneous Transform")
            print (match_target)
            print ("")

            # if scaling:
            #     print ("Total Diff to SA matrix")
            #     print (np.sum(match_target - Tstarg))
            #     print ("")
            # else:
            #     print ("Total Diff to SA matrix")
            #     print (np.sum(match_target - Ttarg))
            #     print ("")

            print ("RMSE:" +  str(rmse))
            print ("If RMSE is near zero, the function is correct!")
f.close()
