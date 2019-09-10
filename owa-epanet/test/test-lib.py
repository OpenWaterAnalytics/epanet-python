from epanet import toolkit

for i in range(1,4):
    p = toolkit.createproject()
    toolkit.deleteproject(p)

p = toolkit.createproject()
del p
