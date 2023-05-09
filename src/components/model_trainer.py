import os
import sys
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {'Linear Regression': LinearRegression(),
          'KNN': KNeighborsRegressor(weights='distance'),
          'Decision Tree': DecisionTreeRegressor(),
          'Random Forest': RandomForestRegressor()}
            params = {'Linear Regression': {'normalize': [True, False]},
          'KNN': {'n_neighbors': [3, 5, 7]},
          'Decision Tree': {'criterion': ['mse', 'friedman_mse'], 'max_depth': [3, 5, 7]},
          'Random Forest': {'n_estimators': [10, 50, 100], 'max_features': ['sqrt', 'log2']}}

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                              models=models,param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            Accuracy_score = r2_score(y_test, predicted)
            return Accuracy_score
            



            
        except Exception as e:
            raise CustomException(e,sys)