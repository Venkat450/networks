import os,sys

import mlflow.sklearn

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_model
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import( RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier)
import mlflow

import dagshub
dagshub.init(repo_owner='Venkat450', repo_name='networks', mlflow=True)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    
    def track_mlflow(self, best_model,classificationmetric):
        with mlflow.start_run():
            f1_score=classificationmetric.f1_score
            precision_score=classificationmetric.precision_score
            recall_score=classificationmetric.recall_score

            

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")
            # Model registry does not work with file store
            # if tracking_url_type_store != "file":

            #     # Register the model
            #     # There are other ways to use the Model Registry, which depends on the use case,
            #     # please refer to the doc for more information:
            #     # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            #     mlflow.sklearn.log_model(best_model, "model", registered_model_name=best_model)
            # else:
            #     mlflow.sklearn.log_model(best_model, "model")

    
        
    def train_model(self, x_train, y_train, x_test,y_test):
        models = {
            "Logistic Regression": LogisticRegression(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        model_report:dict= evaluate_model(x_train,x_test, y_train, y_test, models, params)
        
        ## To get the best model score from the dict
        best_model_score = max(model_report.values())
        
        ## To get the best model name from the dict
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        
        best_model = models[best_model_name]
        
        y_train_pred = best_model.predict(x_train)
        

        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        
        ## Track the experiements with mlflow
        self.track_mlflow(best_model,classification_train_metric)


        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        self.track_mlflow(best_model,classification_test_metric)

        
        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
        
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        
        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, Network_Model)
        save_object("final_model/model.pkl",best_model)
        
        ## Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                      train_metric_artifact=classification_train_metric,
                                                        test_metric_artifact=classification_test_metric)
        logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
        return model_trainer_artifact
        
        
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Initiates the model training process.
        
        :return: ModelTrainerArtifact containing trained model and metrics
        """
        try:
            logging.info("Loading transformed train and test data.")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            # Loading Training and Testing array data
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            x_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]
            
            model_trainer_artifact= self.train_model(x_train, y_train, x_test, y_test)
            
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
                   
        except FileNotFoundError as e:
            raise NetworkSecurityException(e, sys) 