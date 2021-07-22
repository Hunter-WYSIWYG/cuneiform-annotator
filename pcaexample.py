import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import datetime
import numpy as np
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D

from plyfile import PlyData

from sklearn.decomposition import PCA
from sklearn.datasets import make_classification
""" 
The goal is to reduce the dimensionality of a 3D scan from three to two using PCA to cast a shadow of the data onto its two most 
important principal components. Then render the resulting 2D scatter plot.
The scan is a real life armadillo sculpture scanned using a Cyberware 3030 MS 3D scanner at Stanford University. 
The sculpture is available as part of their 3D Scanning Repository, and is a very dense 3D mesh consisting of 172974 vertices! 
The PLY file is available at https://graphics.stanford.edu/data/3Dscanrep/
"""

# Every 100 data samples, we save 1. If things run too
# slow, try increasing this number. If things run too fast,
# try decreasing it... =)
reduce_factor = 100


# Look pretty...
matplotlib.style.use('ggplot')

meshname="test8.ply"
# Load up the scanned armadillo
plyfile = PlyData.read(meshname)
armadillo = pd.DataFrame({
  'x':plyfile['vertex']['x'][::reduce_factor],
  'y':plyfile['vertex']['y'][::reduce_factor],
  'z':plyfile['vertex']['z'][::reduce_factor]
})

the_pca=None
def do_PCA(armadillo):
  #
  # import the libraries required for PCA.
  # Then, train your PCA on the armadillo dataframe. Finally,
  # drop one dimension (reduce it down to 2D) and project the
  # armadillo down to the 2D principal component feature space.
  #
  
  pca = PCA()
  pca.fit(armadillo)
  PCA(copy=True, n_components=3, whiten=False)
  print("=====================")
  print(pca.components_)
  print("=====================")
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_title('PCA, build time: ')
  #ax.scatter(reducedArmadillo[:, 0], reducedArmadillo[:, 1], c='blue', marker='.', alpha=0.75)
  print("Vector "+meshname)
  for length, vector in zip(pca.explained_variance_, pca.components_):
    v = vector * 3 * np.sqrt(length)
    #draw_vector(pca.mean_, pca.mean_ + v)
    print("["+str(pca.mean_)+","+str(pca.mean_+v)+"] Length: "+str(length))
  """
  plt.axis('equal');
  X, y = make_classification(n_samples=10000)
  n_samples = X.shape[0]
  X_centered = X - np.mean(X, axis=0)
  cov_matrix = np.dot(X_centered.T, X_centered) / n_samples
  print(cov_matrix)
  eigenvalues = pca.explained_variance_
  for eigenvalue, eigenvector in zip(eigenvalues, pca.components_):    
    #print(np.dot(eigenvector.T, np.dot(cov_matrix, eigenvector)))
    print(eigenvalue)
    print(eigenvector)
  the_pca=pca
  """
  reducedArmadillo = pca.transform(armadillo)

  return [reducedArmadillo,pca]

"""
def draw_vector(v0, v1, ax=None):
    ax = ax or plt.gca()
    arrowprops=dict(arrowstyle='->',
                    linewidth=2,
                    shrinkA=0, shrinkB=0)
    ax.annotate('', v1, v0, arrowprops=arrowprops)


def do_RandomizedPCA(armadillo):
  #
  # import the libraries required for
  # RandomizedPCA. Then, train your RandomizedPCA on the armadillo
  # dataframe. Finally, drop one dimension (reduce it down to 2D)
  # and project the armadillo down to the 2D principal component
  # feature space.
  #
  #
  # NOTE: SKLearn deprecated the RandomizedPCA method, but still
  # has instructions on how to use randomized (truncated) method
  # for the SVD solver. To find out how to use it, check out the
  # full docs here:
  # http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
  #

  pca = PCA(n_components=2, svd_solver='randomized')
  pca.fit(armadillo)
  PCA(copy=True, n_components=2, whiten=False)

  reducedArmadillo = pca.transform(armadillo)

  return reducedArmadillo


# Render the Original Armadillo
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Armadillo 3D')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.scatter(armadillo.x, armadillo.y, armadillo.z, c='green', marker='.', alpha=0.75)
# plot data


"""
# Time the execution of PCA 5000x
# PCA is ran 5000x in order to help decrease the potential of rogue
# processes altering the speed of execution.
t1 = datetime.datetime.now()
#for i in range(5000): 
pca = do_PCA(armadillo)
time_delta = datetime.datetime.now() - t1
"""
# Render the newly transformed PCA armadillo!
if not pca is None:
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_title('PCA, build time: ' + str(time_delta))
  ax.scatter(pca[0][:,0], pca[0][:,1], c='blue', marker='.', alpha=0.75)
  #plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
  for length, vector in zip(pca[1].explained_variance_, pca[1].components_):
    v = vector * 3 * np.sqrt(length)
    print(pca[1].mean_)
    draw_vector(pca[1].mean_, pca[1].mean_ + v)
   #plt.axis('equal');



# Time the execution of rPCA 5000x
t1 = datetime.datetime.now()
#for i in range(5000): 
rpca = do_RandomizedPCA(armadillo)
time_delta = datetime.datetime.now() - t1

# Render the newly transformed RandomizedPCA armadillo!
if not rpca is None:
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_title('RandomizedPCA, build time: ' + str(time_delta))
  ax.scatter(rpca[:,0], rpca[:,1], c='red', marker='.', alpha=0.75)


plt.show()


soa = np.array([[6.562531,7.3530846,31.809212, -1.835732,-38.796745,29.000275], [ 6.562531,   7.3530846, 31.809212, -19.649292,  12.647268,  23.196705],
                [6.562531,   7.3530846, 31.809212, 4.4853125,  7.3465495, 38.127125]])

X, Y, Z, U, V, W = zip(*soa)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, U, V, W)
ax.set_xlim([-1, 0.5])
ax.set_ylim([-1, 1.5])
ax.set_zlim([-1, 8])
plt.show()"""
