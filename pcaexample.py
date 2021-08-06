import pandas as pd
import matplotlib
import numpy as np

from plyfile import PlyData

from sklearn.decomposition import PCA
from sklearn.datasets import make_classification

meshnames=["H.T._07-31-102_Pulverdruckverfahren_3_Zusammen_mitPuder_mehrPunkte.ply","H.T._07-31-102_SLA_3_Zusammen_mitPuder_mehrPunkte.ply","H.T_07-31-102_FDM_3_Zusammen_mitPuder_mehrPunkte _keine_Nachverarbeitung_mitLoecher.ply", "HT_07-31-47_3D.ply"]

reduce_factors=[1]

reduce_factor = 1

resultfile="result.txt"

def rigid_transform_3D(A, B, scale):
    assert len(A) == len(B)

    N = A.shape[0];  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    print(centroid_A)
    print(centroid_B)

    # center the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    print(AA)
    print(BB)
    print(np.transpose(BB))
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
    print(R)
    print(t)
    print(c)
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
  print("Fake Annotation: [ 1 1 1 ]")
  f.write("Vector "+meshname+"\n")
  counter=1
  resultmatrix=[0,1,2,3]
  for variance, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(variance)
    f.write("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(np.linalg.norm(pca.mean_-(pca.mean_+v)))+"\n")
    resultmatrix[0]=pca.mean_
    resultmatrix[counter]=pca.mean_+v
    counter+=1
  print(resultmatrix)
  print("Fake Annotation Translated: [ "+str(1+pca.mean_[0])+" "+str(1+pca.mean_[1])+" "+str(1+pca.mean_[2])+" ]")
  print("Fake Annotation Translated: [ "+str(1+pca.mean_[0])+" "+str(1+pca.mean_[1])+" "+str(1+pca.mean_[2])+" ]")
  reducedMesh = pca.transform(mesh)
  return [reducedMesh,pca,resultmatrix]

f = open(resultfile, 'w')  
for meshname in meshnames:
    print("Processing "+str(meshname))
    plyfile = PlyData.read(meshname)
    mesh = pd.DataFrame({
    'x':plyfile['vertex']['x'][::reduce_factor],
    'y':plyfile['vertex']['y'][::reduce_factor],
    'z':plyfile['vertex']['z'][::reduce_factor]
    })
    pca = do_PCA(mesh)
    testmatrix=np.matrix([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [3.0,3.0,3.0]])
    testmatrix2=np.matrix([[pca[1].mean_[0]+1, pca[1].mean_[1]+1, pca[1].mean_[2]+1],[pca[1].mean_[0]+2, pca[1].mean_[1]+2, pca[1].mean_[2]+2], [pca[1].mean_[0]+3, pca[1].mean_[1]+3, pca[1].mean_[2]+3]])
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
