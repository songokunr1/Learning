from pyspark.ml.feature import MinMaxScaler
import numpy as np

class BatchedData:

    def __init__(self, data, num_days, scaler=MinMaxScaler()):
        self.scaler = scaler
        self.data = data
        self.num_days = num_days

        # ogólnie zmienne z literą "X" dotyczą zbioru wejściowego, natomiast z literą "Y" dotyczą zbioru wyjściowego

        self.X = self.scaler.fit_transform(self.data.drop(columns=['Data',
                                                                   'Zamkniecie']))  # normalizacja danych i usunięcie kolumn, które nie mają być danymi wejściowymi
        self.y = self.data['Zamkniecie'].values / np.max(
            self.data['Zamkniecie'])  # wartość kolumny "Zamknięcie" jest prognozowana na wyjściu sieci

        self.rng = np.random.randint(1,
                                     len(self.data) - self.num_days)  # losowe wybieranie rekordów do zbiorów testowych i uczących
        self.x_batch = self.X[self.rng:self.rng + self.num_days, :]
        self.y_batch = self.y[self.rng - 1]

    def nextBatch(self):
        rng = np.random.randint(1, len(self.data) - self.num_days)

        while (True):
            rng = np.random.randint(1, len(self.data) - self.num_days)

            if rng != self.rng:
                self.rng = rng
                break

        self.x_batch = self.X[self.rng:self.rng + self.num_days, :].reshape([self.num_days, self.X.shape[1]])
        self.y_batch = self.y[self.rng - 1]

    def createDataset(self):
        train_range = int(len(self.data) * 0.67)  # zbiór uczący
        test_range = int(len(self.data) * 0.33)  # zbiór testowy

        self.X_train = np.zeros([train_range, num_days, self.X.shape[1]])
        self.Y_train = np.zeros([train_range])

        for i in range(train_range):
            self.nextBatch()
            self.X_train[i, :, :] = self.x_batch
            self.Y_train[i] = self.y_batch

        self.X_test = np.zeros([test_range, num_days, self.X.shape[1]])
        self.Y_test = np.zeros([test_range])

        for i in range(test_range):
            self.nextBatch()
            self.X_test[i, :, :] = self.x_batch
            self.Y_test[i] = self.y_batch