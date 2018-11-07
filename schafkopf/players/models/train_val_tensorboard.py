import os
import tensorflow as tf
from keras.callbacks import Callback


class TrainValTensorBoard(Callback):
    def __init__(self, log_dir: str):
        super().__init__()
        self._train_log_dir = os.path.join(log_dir, 'training')
        self._train_writer = None
        self._val_log_dir = os.path.join(log_dir, 'validation')
        self._val_writer = None
        self._trainval_prefix = 'trainval_'

    def set_model(self, model):
        self._train_writer = tf.summary.FileWriter(self._train_log_dir)
        self._val_writer = tf.summary.FileWriter(self._val_log_dir)

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}

        train_logs = {self._trainval_prefix + k: v for k, v in logs.items() if not k.startswith('val_')}
        self.add_log_items_to_writer(self._train_writer, epoch, train_logs)

        val_logs = {k.replace('val_', self._trainval_prefix): v for k, v in logs.items() if k.startswith('val_')}
        self.add_log_items_to_writer(self._val_writer, epoch, val_logs)

    def add_log_items_to_writer(self, writer, epoch, logs):
        for name, value in logs.items():
            if name.replace(self._trainval_prefix, '') in ['batch', 'size']:
                continue
            self.add_value_to_writer(writer, epoch, name, value)
        self._train_writer.flush()

    def add_value_to_writer(self, writer, epoch, name, value):
        summary = tf.Summary()
        summary_value = summary.value.add()
        summary_value.simple_value = value.item()
        summary_value.tag = name
        writer.add_summary(summary, epoch)

    def on_train_end(self, logs=None):
        self._train_writer.close()
        self._val_writer.close()
