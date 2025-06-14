import os

import numpy as np

# import bbobbenchmarks as bbob
from doe2vec import bbobbenchmarks as bbob
from doe2vec import doe2vec

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

import matplotlib.pyplot as plt
from matplotlib import cm


def createSurfacePlot(bbob_fun, gen_fun, dist, name="bbobx", title="f_x" ):
    def no_descs(ax):
        for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
            axis.set_ticklabels([])
            for line in axis.get_ticklines():
                line.set_visible(False)

    fig = plt.figure(figsize=plt.figaspect(0.5))

    # BBOB fun
    X = np.arange(-5, 5, 0.1)
    Y = np.arange(-5, 5, 0.1)
    X, Y = np.meshgrid(X, Y)
    positions = np.vstack([X.ravel(), Y.ravel()]).T
    positions = np.clip(positions, -4.99, 4.99)
    positions = np.where(positions==0, 0.01, positions)
    z1 = np.asarray(list(map(bbob_fun, positions))).reshape(100, 100)

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    # Plot the surface.
    surf = ax.plot_surface(X, Y, z1, cmap=cm.coolwarm, linewidth=1, antialiased=True)
    no_descs(ax)
    plt.title(title)
    # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)

    # Generated fun
    X2 = np.arange(0, 1, 0.01)
    Y2 = np.arange(0, 1, 0.01)
    X2, Y2 = np.meshgrid(X2, Y2)
    array_x = np.vstack([X2.ravel(), Y2.ravel()]).T
    array_x = np.clip(array_x, -0.01, 0.99)
    z2 = gen_fun(array_x)
    # z2 = eval(gen_fun)
    z2 = np.array(z2).reshape(100, 100)
    # second
    ax = fig.add_subplot(1, 2, 2, projection="3d")
    surf = ax.plot_surface(X2, Y2, z2, cmap=cm.coolwarm, linewidth=1, antialiased=True)
    no_descs(ax)
    plt.title(str(dist))

    # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(f"{name}.png")
    # plt.show()


doe = doe2vec.doe_model(dim=2,m=8, latent_dim=16)
doe.load_or_train()

sample = doe.sample * 10 - 5
sample = np.clip(sample, -4.99, 4.99)
sample = np.where(sample==0, 0.01, sample)

for f in range(1, 25):
    for i in [1]:
        fun, opt = bbob.instantiate(f, i)
        name = f"nearest_f_plot/bbob-f-{f}-i-{i}"
        bbob_y = np.asarray(list(map(fun, sample)))
        approx, dist = doe.func_approx(bbob_y,scale=False)
        # print(f, i)
        createSurfacePlot(fun, approx, dist, name, "$f_{" + str(f) + "}$ instance " + str(i))



# obj = doe2vec.doe_model(
#     2, 8, n=250_000, latent_dim=16, model_type="VAE", kl_weight=0.001, use_mlflow=False
# )
# if not obj.loadModel():
#     if not obj.loadData():
#         obj.generateData()
#     obj.compile()
#     obj.fit(20)
#     obj.save()
# sample = obj.sample * 10 - 5
# sample = np.clip(sample, -4.99, 4.99)
# sample = np.where(sample==0, 0.01, sample)

# for f in range(1, 25):
#     for i in [1]:
#         fun, opt = bbob.instantiate(f, i)
#         name = f"nearest_f_plot/bbob-f-{f}-i-{i}"
#         bbob_y = np.asarray(list(map(fun, sample)))
#         array_y = (bbob_y.flatten() - np.min(bbob_y)) / (
#             np.max(bbob_y) - np.min(bbob_y)
#         )
#         encoded = obj.encode([array_y])
#         gen_fun, dist = obj.getNeighbourFunction(encoded)
#         print(f, i, dist)
#         createSurfacePlot(fun, gen_fun, dist, name, "$f_{" + str(f) + "}$ instance " + str(i))