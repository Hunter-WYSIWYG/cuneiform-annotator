import pandas as pd
import matplotlib
import numpy as np
import os

from plyfile import PlyData

from sklearn.decomposition import PCA
from sklearn.datasets import make_classification

input_folder = r"F:\i3mainz_Hochschule Mainz\Keilschriften\neue_orientierung\Neuer Ordner"
# meshnames=["H.T._07-31-102_Pulverdruckverfahren_3_Zusammen_mitPuder_mehrPunkte.ply","H.T._07-31-102_SLA_3_Zusammen_mitPuder_mehrPunkte.ply","H.T_07-31-102_FDM_3_Zusammen_mitPuder_mehrPunkte _keine_Nachverarbeitung_mitLoecher.ply", "HT_07-31-47_3D.ply"]

reduce_factors=[1]

reduce_factor = 1

resultfile=input_folder + "/" + "pca_result.txt"

def rigid_transform_3D(A, B, scale):
    assert len(A) == len(B)

    N = A.shape[0];  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    # print ("centroid A und B .....")
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
        # print("Reflection detected")
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
    wktString+="CS[\"PCA System\",\"cartesian\"]"
    

def do_PCA(mesh): 
  pca = PCA()
  pca.fit(mesh)
  PCA(copy=True, n_components=3, whiten=False)
#   print("Fake Annotation: [ 1 1 1 ]")
  f.write("Mesh "+meshname+"\n")
  for variance, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(variance)
    f.write("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(np.linalg.norm(pca.mean_-(pca.mean_+v)))+"\n")
    print ("in do_PCA Methode")
    print ("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(np.linalg.norm(pca.mean_-(pca.mean_+v)))+"\n")
#   print("Fake Annotation Translated: [ "+str(1+pca.mean_[0])+" "+str(1+pca.mean_[1])+" "+str(1+pca.mean_[2])+" ]")
#   print("Fake Annotation Translated: [ "+str(1+pca.mean_[0])+" "+str(1+pca.mean_[1])+" "+str(1+pca.mean_[2])+" ]")
#   reducedMesh = pca.transform(mesh)

#   return [reducedMesh,pca]
    return [None, pca]

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
            # testmatrix=np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [3.0,3.0,3.0]])
            # testmatrix2=np.array([[pca[1].mean_[0]+1, pca[1].mean_[1]+1, pca[1].mean_[2]+1],[pca[1].mean_[0]+2, pca[1].mean_[1]+2, pca[1].mean_[2]+2], [pca[1].mean_[0]+3, pca[1].mean_[1]+3, pca[1].mean_[2]+3]])
            
            print ("-----")
            print (np.array([[pca[1].mean_[0]+1, pca[1].mean_[1]+1, pca[1].mean_[2]+1],[pca[1].mean_[0]+2, pca[1].mean_[1]+2, pca[1].mean_[2]+2], [pca[1].mean_[0]+3, pca[1].mean_[1]+3, pca[1].mean_[2]+3]]))
            # wir wollen from "Objektkoordinaten" to "pca-Koordianten"
            # Objektkoordinaten
            p0_pca_A = np.array([1.1134167,-1.5002065, 0.8332713])
            p1_pca_A = np.array([-45.707222,-2.560026,1.5315728])
            p2_pca_A = np.array([0.5027458,26.589907,2.520873])
            p3_pca_A = np.array([1.0069973,-1.1094689,-5.709046])
            # pca-Koordinaten
            p0_pca_B= np.array([0,0,0])
            p1_pca_B= np.subtract(p1_pca_A, p0_pca_A)
            p2_pca_B= np.subtract(p2_pca_A, p0_pca_A)
            p3_pca_B= np.subtract(p3_pca_A, p0_pca_A)

            testmatrix = np.matrix([p0_pca_A , p1_pca_A, p2_pca_A, p3_pca_A])
            testmatrix2 = np.matrix([p0_pca_B , p1_pca_B, p2_pca_B, p3_pca_B])

            print ("result pca mesh")
            print (pca)
            
            print ("testmatrizen")
            print(testmatrix)
            print(testmatrix2)

            s, ret_R, ret_t=rigid_transform_3D(testmatrix, testmatrix2,False)

            print("Rotation")
            print(ret_R)
            print("")

            print("Translation") 
            print(ret_t)
            print("")

            print("Scale")
            print(s)
            print("")
f.close()
