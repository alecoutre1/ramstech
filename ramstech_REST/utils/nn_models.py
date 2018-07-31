import keras,kapre


def load_kapre_model(name):
    md = keras.models.load_model(name,
                                    custom_objects={'Melspectrogram': kapre.time_frequency.Melspectrogram,
                                                    'Normalization2D': kapre.utils.Normalization2D})
    return md