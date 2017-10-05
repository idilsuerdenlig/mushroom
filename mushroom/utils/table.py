import numpy as np


class Table(object):
    """
    Table regressor. Used for discrete state and action spaces.

    """
    def __init__(self, shape, initial_value=0.):
        """
        Constructor.

        Args:
            shape (tuple): the shape of the tabular regressor.
            initial_value (float): the initial value for each entry of the
                tabular regressor.

        """
        self.__name__ = 'Table'
        self.table = np.ones(shape) * initial_value

    def __getitem__(self, args):
        idxs = self._get_index(args)
        return self.table[idxs]

    def __setitem__(self, args, value):
        idxs = self._get_index(args)
        self.table[idxs] = value

    def _get_index(self, args):

        if isinstance(args, int):
            idxs = (args,)
        elif len(args) == 1:
            idxs = tuple(args[0].ravel())
        elif type(args[0]) is slice:
            idxs = (args[0],)*(len(self.table.shape)-1) + tuple(args[1].astype(int))
        elif type(args[1]) is slice:
            idxs = tuple(args[0].astype(int))+(args[1],)
        else:
            idxs = tuple(np.concatenate((args[0].astype(int), args[1].astype(int))))

        return idxs


    def fit(self, x, y, **fit_params):
        """
        Fit the model.

        Args:
            x (list): a two elements list with states and actions;
            y (np.array): targets;
            **fit_params (dict): other parameters.

        """
        idxs = tuple(np.concatenate((x[0].astype(int).flatten(), x[1].astype(int).flatten())))
        self.table[idxs] = y[0]

    def predict(self, x):
        """
        Predict.

        Args:
            x (list): a two elements list with states and actions;

        Returns:
            The predictions of the model.

        """
        #assert len(x[0].shape) == len(self.table.shape), 'tabular regressor dimension ' \
        #                                         'does not fit with input size.'

        if x[0].ndim == 2:
            x = np.concatenate((x[0], x[1]), axis=1)
        else:
            x = [x[0], x[1]]

        idxs = [x[:, i].astype(int) for i in xrange(x.shape[1])]
        table = self.table[idxs]

        return table

    def predict_all(self, x, **predict_params):
        table = []

        for i in xrange(len(x)):
            s = x[i]
            val = self[s, :]
            table.append(val)

        return np.array(table)


    @property
    def shape(self):
        return self.table.shape

    def __str__(self):
        return self.__name__