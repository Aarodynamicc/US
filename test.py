import tensorflow as tf

# In TF 1.15 (DirectML), check for available devices this way:
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

# To verify it's actually using the DML device, run a small operation:
tf.enable_eager_execution(tf.ConfigProto(log_device_placement=True))
print(tf.add([1.0, 2.0], [3.0, 4.0]))