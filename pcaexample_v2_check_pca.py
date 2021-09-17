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


# input_folder = r"E:\i3mainz_Hochschule Mainz\Keilschriften\pca\small_meshes"
# input_folder = r"E:\i3mainz_Hochschule Mainz\Keilschriften\pca\test_orientation"
# input_folder = r"E:\temp\Neuer Ordner (7)"
# meshnames=["H.T._07-31-102_Pulverdruckverfahren_3_Zusammen_mitPuder_mehrPunkte.ply","H.T._07-31-102_SLA_3_Zusammen_mitPuder_mehrPunkte.ply","H.T_07-31-102_FDM_3_Zusammen_mitPuder_mehrPunkte _keine_Nachverarbeitung_mitLoecher.ply", "HT_07-31-47_3D.ply"]

# parameter for pca vector calculation
reduce_factors=[1]
reduce_factor = 1
scaling = False
para_stabel = 50  #prozent für stabilität von Längen der pca vektoren 


# # output files
# resultfile=input_folder + "/" + "pca_result.txt"
# resultfile_csv=input_folder + "/" + "pca_result.csv"
# logfile = input_folder + "/" + "pca_log.txt"


#
##### methods  ####
#

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

    trama_A2B= np.asmatrix(trama_A2B)
    trama_A2B = np.transpose(trama_A2B)
    print (trama_A2B)
    print (type(trama_A2B))
    trama_A2B_i = inv(np.matrix(trama_A2B))

    # print ("--- check centroid ---")
    # pc = [0,0,0,1]
    # pc = np.asarray(pc)
    # print (pc)
    # pcn = (np.matmul(pc, trama_A2B))
    # print (pcn)
    # print ("--- check finisch ---")

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
    # f.write("check centroid" +"\n")
    # f.write(str(pc)+"\n")
    # f.write(str(pcn)+"\n")
    
    return c, R, t, rmse, trama_A2B



def transform_points(self, points):
    """
    Given a 4x4 transformation matrix, transform an array of 3D points.
    Expected point foramt: [[X0,Y0,Z0],..[Xn,Yn,Zn]]
    """
    # Needed foramt: [[X0,..Xn],[Z0,..Zn],[Z0,..Zn]]. So let's transpose
    # the point matrix.
    points = points.transpose()
    # Add 0s row: [[X0..,Xn],[Y0..,Yn],[Z0..,Zn],[0,..0]]
    points = np.append(points, np.ones((1, points.shape[1])), axis=0)
    # Point transformation
    points = self * points
    # Return all but last row
    return points[0:3].transpose() 



########## START ################

# output files
input_folder = r"P:\3d-datasets_intern\temp"
resultfile=input_folder + "/" + "pca_result.txt"
checkfile = input_folder + "/" + "check_points_result.csv"

f = open(resultfile, 'w')  
cf = open(checkfile, 'w')
cf.write("file" + "|" + "point-id" + "|" + "x in ref" + "|" + "y in ref" + "|" + "z in ref" + "|" + "x transformiert" + "|" + "y transformiert" + "|" + "z transformiert" + "|" + "x reo check" + "|" + "y reo check" + "|" + "z reo check" + "|" + "diff transformiert - reo check" + "\n")        # Datei
                        

# input
filename = ['HT_05-10-506_3D_reoriented_01','HT_05-10-506_3D_reoriented_02','HT_05-10-506_3D_reoriented_03','HT_05-10-506_3D_reoriented_04','HT_05-10-506_3D_reoriented_05','HT_05-10-506_3D_reoriented_06','HT_05-10-506_3D_reoriented_07']


# reference mesh --> annotations point coordinate
file_ref_points = r"P:\3d-datasets_intern\reoriented_controlled\HT_05-10-506_3D_ref_A-Testpunkte.txt"
# reference mesh --> PCA in Matrix A
file_ref_pca_A = r"P:\3d-datasets_intern\reoriented_controlled\HT_05-10-506_3D_ref_PCA-M-A.txt"
A_ref = np.loadtxt(file_ref_pca_A)
A_ref = np.asmatrix(A_ref)

for file in filename:
    # reoriented Mesh --> PCA in Matrix A
    file_reo01_pca_A = r"P:\3d-datasets_intern\reoriented_controlled//" + file + "_PCA-M-A.txt"
    A_reo = np.loadtxt(file_reo01_pca_A)
    A_reo = np.asmatrix(A_reo)

    # CHECK --> (reoriented)annotations in reoriented mesh
    file_reo_points = r"P:\3d-datasets_intern\reoriented_controlled//" + file + "_A-Testpunkte.txt"

    ## calculate transformation matrix between reference and reoriented meshes
    s, ret_R, ret_t, ret_rmse, ret_pca2obj = rigid_transform_3D(A_ref, A_reo,False)
    ret_pca2obj_i = inv(np.matrix(ret_pca2obj))

    with open (file_ref_points, "r") as file_pkt_ref:
        lines = file_pkt_ref.readlines()
        for line in lines:
            print ("___")
            print (line)
            list_pkt = []
            line = (line.replace("\t"," "))
            line = (line.replace(",",""))
            line = line.split(" ")
            list_pkt.append(float(line[1]))
            list_pkt.append(float(line[2]))
            list_pkt.append(float(line[3]))
            list_pkt.append(float(1))
            print (list_pkt)

            print ("--- transform ref to reo---")
            pc = list_pkt
            pc = np.asarray(pc)
            # print (pc)
            pcn = (np.matmul(pc, ret_pca2obj_i))
            print (pcn)
            print ("--- check finisch ---")

            ### check with reoriented points
            with open (file_reo_points, "r") as file_pkt_reo:
                lines_reo = file_pkt_reo.readlines()
                for line_reo in lines_reo:
                    if (line[0]) in line_reo:
                        print (line_reo)
                        list_pkt_reo = []
                        line_reo = (line_reo.replace("\t"," "))
                        line_reo = (line_reo.replace(",",""))
                        line_reo = line_reo.split(" ")
                        list_pkt_reo.append(float(line_reo[1]))
                        list_pkt_reo.append(float(line_reo[2]))
                        list_pkt_reo.append(float(line_reo[3]))
                        list_pkt_reo.append(float(1))
                        print (list_pkt_reo)
                        diff =np.array([np.linalg.norm(np.array(list_pkt_reo) - np.array(pcn))])
                        print (round(float(diff),3))
                        print("---")

                        cf.write(file + "|")        # Datei
                        cf.write(line[0] + "|")     # Punktbezeichnung
                        cf.write(line[1] + "|")     # x in reference mesh
                        cf.write(line[2] + "|")     # y in reference mesh
                        cf.write(line[3] + "|")     # z in reference mesh
                        cf.write(str(pcn.item(0)) + "|")     # x in new mesh
                        cf.write(str(pcn.item(1)) + "|")     # y in new mesh
                        cf.write(str(pcn.item(2)) + "|")     # z in new mesh
                        cf.write(line_reo[1] + "|")     # x check point from reoriented mesh
                        cf.write(line_reo[2] + "|")     # x check point from reoriented mesh
                        cf.write(line_reo[3] + "|")     # x check point from reoriented mesh
                        cf.write(str(round(float(diff),3)) + "\n")     # diff from check point with transformation


f.close()
cf.close()


print ("fertsch :-|")