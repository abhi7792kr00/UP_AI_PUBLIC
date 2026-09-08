import pandas as pd
from pathlib import Path


def read_csv(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"❌ File not found : {file_path}")
        return None

    df = pd.read_csv(path)

    print(f"✅ Loaded {len(df)} Records")

    return df