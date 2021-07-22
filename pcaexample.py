import pandas as pd
import numpy as np

from plyfile import PlyData

from sklearn.decomposition import PCA

meshnames=["test.ply","test2.ply","test3.ply","test4.ply","test5.ply","test6.ply","test7.ply","test8.ply"]

reduce_factor = 100

resultfile="result.txt"
f = open(resultfile, 'w')

def do_PCA(mesh): 
  pca = PCA()
  pca.fit(mesh)
  PCA(copy=True, n_components=3, whiten=False)
  f.write("Vector "+meshname+"\n")
  for length, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(length)
    f.write("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(length)+"\n")
  reducedMesh = pca.transform(mesh)
  return [reducedMesh,pca]

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
