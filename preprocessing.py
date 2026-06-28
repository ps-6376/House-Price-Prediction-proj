from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import app
def preprocesse():
        house_data=pd.read_csv("housing.csv")
        x=house_data.drop("median_house_value",axis=1)
        y=house_data["median_house_value"]
        print(x)
        print(y)
        s=StratifiedShuffleSplit(n_splits=1, test_size=0.2)
        obj=s.split(x,x["ocean_proximity"])
        indexes=obj.__next__() 
        print(indexes)
        train_inx=indexes[0]
        test_inx=indexes[1]
        x_train=x.iloc[train_inx]
        y_train=y.iloc[train_inx]
        x_test=x.iloc[test_inx]
        y_test=y.iloc[test_inx]
        print(x_train)
        print(y_train)
        print(x_test)
        print(y_test)

        num_col=house_data.columns[:-2]
        cat_col=house_data.columns[9:]
        num_pipeline=Pipeline([
            ("impute",SimpleImputer(strategy="median")),
            ("scale", StandardScaler())
        ])
        cat_pipeline= Pipeline([
            ("cat_impute",SimpleImputer(strategy="most_frequent")),
            ("odinal",OrdinalEncoder())
        ])
        final_pipeline=ColumnTransformer([
            ("num_pipeline",num_pipeline,num_col),
            ("cat_pipeline",cat_pipeline,cat_col)
        ])
        final_pipeline.fit(x_train)
        x_train_tr=final_pipeline.transform(x_train)
        x_test_tr=final_pipeline.transform(x_test)
        return (x_train_tr,x_test_tr,y_train)
preprocesse()





