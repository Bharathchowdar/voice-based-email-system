import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions


class ImageCaptioner:
    def __init__(self):
        print("[ImageCaptioner] Loading InceptionV3 model...")
        self.model = InceptionV3(weights='imagenet')
        print("[ImageCaptioner] Model loaded.")

    def caption(self, image_data: bytes) -> str:
        """Generate a descriptive caption for an image given its raw bytes."""
        try:
            img = Image.open(io.BytesIO(image_data)).convert('RGB')
            img = img.resize((299, 299))
            img_array = np.array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            predictions = self.model.predict(img_array)
            decoded = decode_predictions(predictions, top=3)[0]

            labels = [label for (_, label, _) in decoded]
            confidence = decoded[0][2]

            caption = f"This image appears to contain: {', '.join(labels)}. " \
                      f"Most likely: {labels[0]} with {confidence * 100:.1f}% confidence."
            return caption

        except Exception as e:
            print(f"[Captioner Error]: {e}")
            return "Could not generate a description for this image."
