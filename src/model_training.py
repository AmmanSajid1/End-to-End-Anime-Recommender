import joblib 
import numpy as np 
import os 
import sys
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from src.logger import get_logger
from utils.common_functions import read_yaml
from src.custom_exception import AppException
from src.base_model import BaseModel 
from config.paths_config import * 

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, config_path):
        self.config = read_yaml(config_path)
        logger.info("Model Training Initialized")

    def load_data(self):
        try:
            X_train_array = joblib.load(X_TRAIN_ARRAY)
            X_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_TEST)

            logger.info("Data loaded successfully for model training")
            return X_train_array, X_test_array, y_train, y_test
        
        except Exception as e:
            raise AppException(e, sys)
        
    
    def train_model(self):
        try:
            X_train_array, X_test_array, y_train, y_test = self.load_data()
            
            n_users = len(joblib.load(USER2USER_ENCODED))
            n_anime = len(joblib.load(ANIME2ANIME_ENCODED))

            base_model = BaseModel(config_path=CONFIG_PATH)

            model = base_model.RecommenderNet(n_users, n_anime)

            epochs = int(self.config["model"]["epochs"])
            start_lr = float(self.config["model"]["start_lr"])
            max_lr = float(self.config["model"]["max_lr"])
            min_lr = float(self.config["model"]["min_lr"])
            batch_size = int(self.config["model"]["batch_size"])
            ramup_epochs = int(self.config["model"]["ramup_epochs"])
            sustain_epochs = int(self.config["model"]["sustain_epochs"])
            exp_decay = float(self.config["model"]["exp_decay"])

            def lrfn(epoch):
                if epoch < ramup_epochs:
                    return(max_lr - start_lr)/ramup_epochs*epoch+start_lr
                
                elif epoch<ramup_epochs+sustain_epochs:
                    return max_lr 
                
                else:
                    return (max_lr - min_lr) * exp_decay ** (epoch-ramup_epochs-sustain_epochs) + min_lr
                
            lr_callback = LearningRateScheduler(lambda epoch:lrfn(epoch), verbose=0)
            model_checkpoint = ModelCheckpoint(filepath=CHECKPOINT_FILE_PATH, save_weights_only=True, monitor="val_loss", mode="min", save_best_only=True)
            early_stopping = EarlyStopping(patience=3, monitor="val_loss", mode="min", restore_best_weights=True)  
            my_callbacks = [model_checkpoint, lr_callback, early_stopping]

            os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH), exist_ok=True)
            os.makedirs(MODEL_DIR, exist_ok=True)
            os.makedirs(WEIGHTS_DIR, exist_ok=True) 

            try:
                history = model.fit(
                    x = X_train_array,
                    y = y_train,
                    batch_size = batch_size,
                    epochs = epochs,
                    verbose=1,
                    validation_data = (X_test_array, y_test),
                    callbacks=my_callbacks
                )

                model.load_weights(CHECKPOINT_FILE_PATH)
                logger.info("Model Training Completed")

            except Exception as e:
                raise AppException(e,sys) from e 
            
            self.save_model_weights(model)
            
        except Exception as e:
            raise AppException(e,sys) from e 
        
    def extract_weights(self, name, model):
        try:
            weight_layer = model.get_layer(name)
            weights = weight_layer.get_weights()[0]
            weights = weights/np.linalg.norm(weights, axis=1).reshape((-1, 1))
            logger.info(f"Extracting weights for layer {name}")
            return weights 

        except Exception as e:
            raise AppException(e,sys) from e 
        
    
    def save_model_weights(self, model):
        try:
            model.save(MODEL_PATH)
            logger.info(f"Model saved to {MODEL_PATH}")

            user_weights = self.extract_weights("user_embedding", model)
            anime_weights = self.extract_weights("anime_embedding", model)

            joblib.dump(user_weights, USER_WEIGHTS_PATH)
            joblib.dump(anime_weights, ANIME_WEIGHTS_PATH)

            logger.info("User and Anime weights saved successfully")

        except Exception as e:
            raise AppException(e,sys) from e
        
if __name__ == "__main__":
    model_trainer = ModelTraining(CONFIG_PATH)
    model_trainer.train_model()



            