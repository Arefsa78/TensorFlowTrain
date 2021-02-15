from make_data import make_all
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
from numpy import array
import pandas as pd

headers = []
X, Y = make_all(headers)
X = array(X)
Y = array(Y)
print(headers)

model = ExtraTreesClassifier()
model.fit(X, Y)
print(model.feature_importances_)  # use inbuilt class feature_importances of tree based classifiers
# plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=headers)
feat_importances.plot(kind='barh')
plt.show()
