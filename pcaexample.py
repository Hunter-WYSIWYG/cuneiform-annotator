import pandas as pd
import matplotlib
import numpy as np

from plyfile import PlyData

from sklearn.decomposition import PCA
from sklearn.datasets import make_classification

meshnames=["test.ply","test2.ply","test3.ply","test4.ply","test5.ply","test6.ply","test7.ply","test8.ply"]

reduce_factors=[1,10,100,1000]

reduce_factor = 1

resultfile="result.txt"


def do_PCA(mesh): 
  pca = PCA()
  pca.fit(mesh)
  PCA(copy=True, n_components=3, whiten=False)
  f.write("Vector "+meshname+"\n")
  for i in range(len(pca.components_)):
    PC = list(zip(pca.mean_-2*pca.components_[i],pca.mean_+1*pca.components_[i]))
    print(PC)
    #ax.plot(PC[0],PC[1],PC[2],cols[i])
  for length, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(length)
    f.write("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(np.linalg.norm(pca.mean_-(pca.mean_+v)))+"\n")
  reducedMesh = pca.transform(mesh)
  return [reducedMesh,pca]

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
f.close()
