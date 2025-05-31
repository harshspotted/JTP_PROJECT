import keras
from keras import ops
from keras import layers
from keras import Model


# Modular Tower Block
class ResidualBlock(layers.Layer):
    def __init__(self, emb_size, dropout_rate=0.2, **kwargs):
        super().__init__(**kwargs)
        self.dense = layers.Dense(emb_size, activation=None)
        self.bn = layers.BatchNormalization()
        self.act = layers.Activation("relu")
        self.drop = layers.Dropout(dropout_rate)

    def call(self, x, training=False):
        y = self.dense(x)
        y = self.bn(y, training=training)
        y = self.act(y)
        y = self.drop(y, training=training)
        return x + y


@keras.saving.register_keras_serializable()
class Tower(keras.Model):
    def __init__(
        self,
        emb_size: int = 32,
        depth: int = 3,
        dropout_rate: float = 0.2,
        name: str = "tower",
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.emb_size = emb_size
        self.depth = depth
        self.dropout_rate = dropout_rate

        # Initial projection
        self.init_num = layers.Dense(
            emb_size, activation="relu", name=f"{name}_init_num"
        )
        self.init_txt = layers.Dense(
            emb_size, activation="relu", name=f"{name}_init_txt"
        )

        # Stacked residual blocks
        self.blocks_num = [
            ResidualBlock(emb_size, dropout_rate, name=f"{name}_res_num_{i}")
            for i in range(depth)
        ]
        self.blocks_txt = [
            ResidualBlock(emb_size, dropout_rate, name=f"{name}_res_txt_{i}")
            for i in range(depth)
        ]
        self.add = layers.Add(name=f"{name}_add")

    def call(self, inputs, training=False):
        num_input, txt_input = inputs
        x_num = self.init_num(num_input)
        x_txt = self.init_txt(txt_input)
        for block in self.blocks_num:
            x_num = block(x_num, training=training)
        for block in self.blocks_txt:
            x_txt = block(x_txt, training=training)
        return self.add([x_num, x_txt])

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "emb_size": self.emb_size,
                "depth": self.depth,
                "dropout_rate": self.dropout_rate,
            }
        )
        return config


@keras.saving.register_keras_serializable()
class TwoTowerModel(keras.Model):
    def __init__(
        self, emb_size: int = 32, depth: int = 3, dropout_rate: float = 0.2, **kwargs
    ):
        super().__init__(**kwargs)
        self.emb_size = emb_size
        self.depth = depth
        self.dropout_rate = dropout_rate

        self.employee_tower = Tower(
            emb_size, depth, dropout_rate, name="employee_tower"
        )
        self.project_tower = Tower(emb_size, depth, dropout_rate, name="project_tower")
        self.dot = layers.Dot(axes=1, name="dot_similarity")

    def call(self, inputs, training=False):
        employee_num, employee_txt, project_num, project_txt = inputs
        employee_emb = self.employee_tower(
            [employee_num, employee_txt], training=training
        )
        project_emb = self.project_tower([project_num, project_txt], training=training)
        return self.dot([employee_emb, project_emb])

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "emb_size": self.emb_size,
                "depth": self.depth,
                "dropout_rate": self.dropout_rate,
            }
        )
        return config


def build_model(
    n_skills: int,
    text_emb_size: int,
    emb_size: int = 32,
    depth: int = 3,
    dropout_rate: float = 0.2,
) -> keras.Model:
    """
    Builds the enhanced two-tower model with residual blocks, normalization, and dropout.

    Args:
        n_skills: Dimensionality of numeric input.
        text_emb_size: Dimensionality of text embedding input.
        emb_size: Output embedding size for each tower.
        depth: Number of residual blocks per tower.
        dropout_rate: Dropout rate for residual blocks.

    Returns:
        A compiled Keras Model.
    """
    employee_num = keras.Input(shape=(n_skills,), name="employee_num")
    employee_txt = keras.Input(shape=(text_emb_size,), name="employee_txt")
    project_num = keras.Input(shape=(n_skills,), name="project_num")
    project_txt = keras.Input(shape=(text_emb_size,), name="project_txt")
