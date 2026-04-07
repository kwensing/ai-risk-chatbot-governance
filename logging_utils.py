import pandas as pd

def log_interaction(user_input, response, score, level):
    df = pd.DataFrame([{
        "input": user_input,
        "response": response,
        "risk_score": score,
        "risk_level": level
    }])
    df.to_csv("logs.csv", mode="a", header=False, index=False)