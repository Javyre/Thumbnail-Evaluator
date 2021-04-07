import keras
import numpy as np

class Model:
    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)

    def predict(self, image):
        from keras.preprocessing.image import load_img, img_to_array
        image_arr = img_to_array(load_img(image, target_size=(128, 128)))
        predictions = self.model.predict(np.array([image_arr]))
        predictions = np.argmax(predictions, axis=1)
        return predictions[0]
