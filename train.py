import boto3
import pandas as pd
import io
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# set aws credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id="AKIARMLDB7OHP5IFHFC2",
    aws_secret_access_key="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",
)
BUCKET_NAME = "hajong-data"
object_key = 'data/6c/5869cfe7c8f8efb7ed2c840b5bdb02'
object_ = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_key)
df = pd.read_csv(io.BytesIO(object_["Body"].read()))


drop_cols = ["Name", "Cabin", "Ticket", "PassengerId"]
df = df.drop(columns=drop_cols)
df = df.fillna(value={"Age": df["Age"].mean(), "Embarked": "S"})

encoder = LabelEncoder()

df["Sex"] = encoder.fit_transform(df[["Sex"]])
df["Embarked"] = encoder.fit_transform(df[["Embarked"]])
y = df.pop("Survived")
X = df
train_X, valid_X, train_y, valid_y = train_test_split(
    X, y.values.ravel(), test_size=0.2, random_state=42
)
clf = RandomForestClassifier()
clf.fit(train_X, train_y)
pred = clf.predict_proba(valid_X)
score = roc_auc_score(valid_y, pred[:, 1])
print(score)
