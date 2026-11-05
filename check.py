import tensorflow as tf

# Load your TFLite model
interpreter = tf.lite.Interpreter(model_path="exercise_model.tflite")

# Get signature list
signatures = interpreter.get_signature_list()
print(signatures)
