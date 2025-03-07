import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# ✅ Step 1: Generate Synthetic Data (500 samples, realistic distribution)
np.random.seed(42)
num_samples = 500

synthetic_data = {
    "autonomy": np.random.normal(7, 2, num_samples).clip(1, 10),
    "relatedness": np.random.normal(8, 1.5, num_samples).clip(1, 10),
    "competence": np.random.normal(6, 2, num_samples).clip(1, 10),
    "vitality": np.random.normal(7, 2, num_samples).clip(1, 10),
    "social_comparison": np.random.normal(5, 2.5, num_samples).clip(1, 10),
    "monetary_impact": np.random.normal(0, 15, num_samples).clip(-50, 50),
}

df = pd.DataFrame(synthetic_data)

# Define a "true" Experience Value (EV) score using a weighted sum + noise
true_weights = np.array([0.25, 0.2, 0.2, 0.15, 0.1, 0.1])
df["experience_value"] = np.dot(df[list(synthetic_data.keys())], true_weights) + np.random.normal(0, 2, num_samples)

# ✅ Step 2: Train the Regression Model
X = df.drop(columns=["experience_value"])
y = df["experience_value"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# ✅ Step 3: Test the Model
predictions = model.predict(X_test)

# ✅ Step 4: Display Results
# Model accuracy (R² score)
model_accuracy = model.score(X_test, y_test)
print(f"\n✅ Model Accuracy (R² Score): {model_accuracy:.4f}\n")

# Regression Coefficients (Impact of each factor on EV)
coefficients = pd.DataFrame({"Factor": X.columns, "Coefficient": model.coef_})
print("\n📊 Regression Coefficients (Impact of Each Factor on EV):")
print(coefficients)

# Show sample predictions (Actual vs Predicted EV)
sample_predictions = pd.DataFrame({"Actual EV": y_test[:10].values, "Predicted EV": predictions[:10]})
print("\n🔍 Sample EV Predictions (First 10 Entries):")
print(sample_predictions)
