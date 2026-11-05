import numpy as np,joblib,tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense,Dropout,Bidirectional
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix, classification_report

X=np.load("X.npy")
y=np.load("y.npy")
train_idx=np.load("train_idx.npy")
test_idx=np.load("test_idx.npy")

N,T,F=X.shape

scaler=StandardScaler()
X=scaler.fit_transform(X.reshape(-1,F)).reshape(N,T,F)
X=np.clip(X,-3,3)

joblib.dump(scaler,"model/scaler.pkl")

X_train,y_train=X[train_idx],y[train_idx]
X_test,y_test=X[test_idx],y[test_idx]

classes=np.unique(y_train)
weights=compute_class_weight("balanced",classes=classes,y=y_train)
class_weights=dict(zip(classes,weights))

X_train+=np.random.normal(0,0.03,X_train.shape)

y_train=to_categorical(y_train)
y_test=to_categorical(y_test)

model=Sequential([
    Bidirectional(LSTM(64,return_sequences=True),input_shape=(T,F)),
    Dropout(0.3),
    LSTM(32),
    Dropout(0.3),
    Dense(64,activation='relu'),
    Dense(4,activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(
    X_train,y_train,
    validation_data=(X_test,y_test),
    epochs=40,
    batch_size=32,
    class_weight=class_weights,
    callbacks=[tf.keras.callbacks.EarlyStopping(patience=5,restore_best_weights=True)]
)

model.save("model/exercise_model.h5")


# =========================
# PREDICTIONS
# =========================
y_pred = model.predict(X_test)

y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_true_classes, y_pred_classes)

print("\nConfusion Matrix:")
print(cm)

# =========================
# CLASSIFICATION REPORT
# =========================
labels = ["squat", "pushup", "pullup", "idle"]

print("\nClassification Report:")
print(classification_report(y_true_classes, y_pred_classes, target_names=labels))