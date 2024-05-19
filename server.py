from http.client import HTTPException
from fastapi import FastAPI # type: ignore
import joblib # type: ignore
import numpy as np # type: ignore
from tensorflow.keras.models import load_model
from tensorflow.keras import layers
from keras import ops
import keras
import cv2
from sklearn.preprocessing import LabelEncoder


app = FastAPI()

class Patches(layers.Layer):
    def __init__(self, patch_size, dtype='float32', **kwargs):
        super().__init__(dtype=dtype, **kwargs)
        self.patch_size = patch_size

    def call(self, images):
        input_shape = ops.shape(images)
        batch_size = input_shape[0]
        height = input_shape[1]
        width = input_shape[2]
        channels = input_shape[3]
        num_patches_h = height // self.patch_size
        num_patches_w = width // self.patch_size
        patches = keras.ops.image.extract_patches(images, size=self.patch_size)
        patches = ops.reshape(
            patches,
            (
                batch_size,
                num_patches_h * num_patches_w,
                self.patch_size * self.patch_size * channels,
            ),
        )
        return patches

    def get_config(self):
        config = super().get_config()
        config.update({"patch_size": self.patch_size})
        return config
    

class PatchEncoder(layers.Layer):
    def __init__(self, num_patches, projection_dim, dtype='float32', **kwargs):
        super().__init__(dtype=dtype, **kwargs)
        self.num_patches = num_patches
        self.projection = layers.Dense(units=projection_dim)
        self.position_embedding = layers.Embedding(
            input_dim=num_patches, output_dim=projection_dim
        )

    def call(self, patch):
        positions = ops.expand_dims(
            ops.arange(start=0, stop=self.num_patches, step=1), axis=0
        )
        projected_patches = self.projection(patch)
        encoded = projected_patches + self.position_embedding(positions)
        return encoded

    def get_config(self):
        config = super().get_config()
        config.update({
            "num_patches": self.num_patches,
            "projection_dim": self.projection.units  # Include projection_dim in the config
        })
        return config

model_path = "./model/vit_model_v3.keras"
loaded_model = load_model(model_path, custom_objects={"Patches": Patches, "PatchEncoder": PatchEncoder})


# Define labels and initialize LabelEncoder
labels = ['enjoying', 'studying']
label_encoder = LabelEncoder()
# Fit and transform labels
encoded_labels = label_encoder.fit_transform(labels)


@app.get('/')
def get_root():
    return {'message': 'Tracking activityes API'}

@app.post('/predict')
def predict(data: dict):
    try:
        image = np.array(data['feature'])
        resized_image = cv2.resize(image, (224, 224))
        prediction = loaded_model.predict(np.expand_dims(resized_image, axis=0))
        predicted_labels = label_encoder.inverse_transform(prediction.argmax(axis=1))
        return {'predicted_class': predicted_labels.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))