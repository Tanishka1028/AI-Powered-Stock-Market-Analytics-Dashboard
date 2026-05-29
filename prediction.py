from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def predict_prices(df):

    df = df.dropna().copy()

    df["Target"] = df["Close"].shift(-1)

    # Remove the last row because Target will be NaN
    df = df[:-1]

    X = df[["Close", "Volume", "MA50", "MA200", "RSI"]]
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    # Predict next day's price
    future_prediction = model.predict(X.iloc[[-1]])

    return future_prediction[0]