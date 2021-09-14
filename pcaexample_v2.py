import pandas as pd
import matplotlib
import numpy as np
import os
import os.path
from math import sqrt
from numpy.linalg import inv
from plyfile import PlyData
from sklearn.decomposition import PCA
from sklearn.datasets import make_classification



input_folder = r"D:\i3mainz_Hochschule Mainz\Keilschriften\pca\small_meshes"
# input_folder = r"E:\temp\Neuer Ordner (7)"
# meshnames=["H.T._07-31-102_Pulverdruckverfahren_3_Zusammen_mitPuder_mehrPunkte.ply","H.T._07-31-102_SLA_3_Zusammen_mitPuder_mehrPunkte.ply","H.T_07-31-102_FDM_3_Zusammen_mitPuder_mehrPunkte _keine_Nachverarbeitung_mitLoecher.ply", "HT_07-31-47_3D.ply"]

# parameter for pca vector calculation
reduce_factors=[1]
reduce_factor = 1
scaling = False
para_stabel = 50  #prozent für stabilität von Längen der pca vektoren 


# output files
resultfile=input_folder + "/" + "pca_result.txt"
resultfile_csv=input_folder + "/" + "pca_result.csv"
logfile = input_folder + "/" + "pca_log.txt"


#
##### methods  ####
#


# pca for a mesh
# input mesh as *.ply
# output reducedMesh (?), pca (?), resultmatrix (?), Matrix A, Matrix B
# es wird hier schon etwas in die Datei (f =  "pca_result.txt") geschrieben .... 
# und in die Datei (c = "pca_result.csv")
def do_PCA(mesh,para_stabel): 
    pca = PCA()
    pca.fit(mesh)
    PCA(copy=True, n_components=3, whiten=False)
    f.write("......................" + "\n"+ "\n")
    f.write("Vector, Mesh "+meshname+"\n"+ "\n")
    f.write("pca" + "\n")
    counter=1
    resultmatrix=[0,1,2,3]
    for variance, vector in zip(pca.explained_variance_, pca.components_):
        v = vector * 3 * np.sqrt(variance) 
        f.write("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(np.linalg.norm(pca.mean_-(pca.mean_+v)))+"\n")
        resultmatrix[0]=pca.mean_
        resultmatrix[counter]=pca.mean_+v
        counter+=1
    reducedMesh = pca.transform(mesh)

    pca = [reducedMesh,pca,resultmatrix]

    ## calculate matrix from pca vectors
    # pca vector coordinates in crs from mesh
    p0_pca_A = pca[2][0]
    p1_pca_A = pca[2][1]
    p2_pca_A = pca[2][2]
    p3_pca_A = pca[2][3]
    # matrix A
    mat_A = np.matrix([p0_pca_A , p1_pca_A, p2_pca_A, p3_pca_A])

    # pca vector coordinates in local defined pca crs
    p0_pca_B= np.array([0,0,0])
    p1_pca_B= np.array([np.linalg.norm(p0_pca_A - p1_pca_A),0,0])
    p2_pca_B= np.array([0,np.linalg.norm(p0_pca_A - p2_pca_A),0])
    p3_pca_B= np.array([0,0,np.linalg.norm(p0_pca_A - p3_pca_A)])
    # matrix B
    mat_B = np.matrix([p0_pca_B , p1_pca_B, p2_pca_B, p3_pca_B])

    # distance / length from pca-vectors
    dist_v1 = np.linalg.norm(p0_pca_A - p1_pca_A)
    dist_v2 = np.linalg.norm(p0_pca_A - p2_pca_A)
    dist_v3 = np.linalg.norm(p0_pca_A - p3_pca_A)

    # differences between the vector lengths in mm and %
    # in unit mm
    diff_v1_v2 = dist_v1 - dist_v2
    diff_v2_v3 = dist_v2 - dist_v3
    # in prozent 
    diff_v1_v2_p = 100 * (dist_v1 - dist_v2) / dist_v1
    diff_v2_v3_p = 100 * (dist_v2 - dist_v3) / dist_v2

    # stabil ???
    if diff_v1_v2 > dist_v1*para_stabel/100 and diff_v2_v3 > dist_v2*para_stabel/100:
        stabil = True
    else:
        stabil = False

    # write in file
    # f.write("Matrix A" +"\n")
    # f.write(str(mat_A)+"\n")
    # f.write("Matrix B" +"\n")
    # f.write(str(mat_B)+"\n")

    f.write("\n")
    f.write(" " + str(para_stabel) + "% " + "\n")
    f.write(" vector 1: " + str(dist_v1) + " " + str(para_stabel) + "% " + str(dist_v1*para_stabel/100) +"\n")
    f.write(" vector 2: " + str(dist_v2) + " " + str(para_stabel) + "% " +  str(dist_v2*para_stabel/100) +"\n")
    f.write(" vector 3: " + str(dist_v3) + " " + str(para_stabel) + "% " +  str(dist_v3*para_stabel/100) +"\n")

    f.write(" differenzen" +"\n")
    f.write(" diff v1-v2: " + str(round((diff_v1_v2),1)) + " mm = " + str(round((diff_v1_v2_p),1)) + "% von vector 1 \n")
    f.write(" diff v2-v3: " + str(round((diff_v2_v3),1)) + " mm = " + str(round((diff_v2_v3_p),1)) + "% von vector 2 \n")

    f.write("\n" + "--->>> pca stabil: " + str(stabil) + "\n" )


    c.write(meshname + "|" + str(round((dist_v1),2)) + "|" + str(round((dist_v2),2)) + "|" + str(round((dist_v3),2)) + "|" + str(round((diff_v1_v2),2)) + "|" + str(round((diff_v1_v2_p),2)) + "|" + str(round((diff_v2_v3),2)) + "|" + str(round((diff_v2_v3_p),2)) + "|" + str(stabil)  + "\n")

    return [reducedMesh,pca,resultmatrix,mat_A,mat_B]


# transformation helmert (?)
# input matrix A (3d point coordinates in coordinate system A)
# input matrix B (3d point coordinates in coordinate system B)
# input scale (?) True/False
# output scale (c), translation (t) , rotation (R), errror (rmse), transformationsmatrix 4x4 (trama_A2B)
def rigid_transform_3D(A, B, scale):
    assert len(A) == len(B)
    N = A.shape[0];  # total points

    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # center the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

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
               
    n = B.shape[0]

    ## Find the error
    B2 = (R * B.T) + np.tile(t, (1, n))
    B2 = B2.T
    err = A - B2
    err = np.multiply(err, err)
    err = np.sum(err)
    rmse = sqrt(err / n)

    ##convert to 4x4 transform
    trama_A2B = np.zeros((4,4))
    trama_A2B[:3,:3] = R
    trama_A2B[0,3] = t[0]
    trama_A2B[1,3] = t[1]
    trama_A2B[2,3] = t[2]
    trama_A2B[3,3] = 1

    # trama_B2A = inv(np.matrix(trama_A2B))
    
    f.write("\n" + "Transformation" + "\n" + "\n")
    f.write("from Matrix"+"\n")
    f.write(str(A)+"\n")
    f.write("to Matrix"+"\n")
    f.write(str(B)+"\n")
    f.write( "\n"+ "result" + "\n")
    f.write("Rotation" +"\n")
    f.write(str(R)+"\n")
    f.write("Translation" +"\n")
    f.write(str(t)+"\n")
    f.write("Scale" +"\n")
    f.write(str(c)+"\n")
    f.write("RMSE" +"\n")
    f.write(str(rmse)+"\n")
    f.write("Homogeneous Transform trama_A2B" +"\n")
    f.write(str(trama_A2B)+"\n")
    
    
    return c, R, t, rmse, trama_A2B


# pca to wkt (?)
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







##################### START ###########################

# control of the processed mesh files
# previousresults=""
# if os.path.isfile(resultfile_csv):
#     print("Found old result file: "+str(resultfile_csv))
#     file = open(resultfile_csv)
#     previousresults=file.read()
#     file.close()

f = open(resultfile, 'w')  
c = open(resultfile_csv, 'w')
l = open(logfile, 'w')
c.write("meshname|vector-1_length|vector-2_length|vector-3_length|diff v1-v2 mm|diff v1-v2 % v1|diff v2-v3 mm|diff v2-v3 % v2|stabil (" + str(para_stabel) + "%)"+"\n")



for root, dirs, files in os.walk (input_folder):
    for meshname in files:
        # print (meshname)
        # if meshname in previousresults:
        #     print("Skipping "+str(meshname)+" as it was already processed!")
        #     continue
        if os.path.splitext(meshname)[-1]==".ply" or os.path.splitext(meshname)[-1]==".PLY":
            # try:
                # files 
                f.close()
                f = open(resultfile, 'a')
                c.close()
                c = open(resultfile_csv, 'a')
                l.close()
                l = open(logfile, 'a')

                # open mesh and define for pca calculation
                print (meshname)
                print("Processing "+str(meshname))
                plyfile = PlyData.read(root + "/" + meshname)
                mesh = pd.DataFrame({
                'x':plyfile['vertex']['x'][::reduce_factor],
                'y':plyfile['vertex']['y'][::reduce_factor],
                'z':plyfile['vertex']['z'][::reduce_factor]
                })

                ## methode do_PCA
                pca = do_PCA(mesh,para_stabel)
                # Matrix A / B
                A = pca[3]
                B = pca[4]      
                # speichern der Matrizen in separaten txt-Dateien
                with open ((root + "//" + meshname.replace(".ply", "_PCA-M-A.txt")), "wb") as file_npy_MA:
                    np.savetxt(file_npy_MA, A)
                file_npy_MA.close()
                with open ((root + "//" + meshname.replace(".ply", "_PCA-M-B.txt")), "wb") as file_npy_MB:
                    np.savetxt(file_npy_MB, B)
                file_npy_MB.close()

                # ## von hier in Methode zur Transformation ???
                # # return = c, R, t, rmse, pca2obj
                s, ret_R, ret_t, ret_rmse, ret_pca2obj = rigid_transform_3D(A, B,False)

                # speichern der Transformationsmatrix in einer separaten Datei
                with open ((root + "//" + meshname.replace(".ply", "_PCA-TM-A2B.txt")), "wb") as file_npy_TM:
                    np.savetxt(file_npy_TM, ret_pca2obj)
                file_npy_TM.close()

                print(A)
                print (B)
                print (ret_pca2obj)     

f.close()
c.close()
l.close()

print ("fertsch")
