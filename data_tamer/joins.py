import unidecode
from thefuzz import fuzz
from thefuzz import process
import pandas as pd


def similarity_join(df1, df2, on, how="outer", threshold=0.9):
    """
    Currentley, the function only supports the
        - levenshtein algorithm
        - outer join
    """

    col1, col2 = on

    # Function to apply the matching
    def match_row(row, df2_col):
        best_match, best_score, x = process.extractOne(row[col1], df2_col)
        if best_score / 100 >= threshold:
            return pd.Series([best_match, best_score])
        else:
            return pd.Series([None, None])

    # Apply the matching function to the first DataFrame
    df1[["best_match", "score"]] = df1.apply(match_row, axis=1, df2_col=df2[col2])

    # Merge the DataFrames
    result_df = pd.merge(df1, df2, left_on="best_match", right_on=col2, how=how)
    result_df.drop(["best_match"], axis=1, inplace=True)

    # Rearrange the columns
    align_cols = list(on) + ["score"]
    result_df = result_df[[col for col in result_df.columns if col not in align_cols] + align_cols]

    result_df = result_df.fillna("")

    return result_df
