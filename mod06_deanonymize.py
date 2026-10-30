import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """

    q_ids = []
    for col in anon_df.columns:
        if col in aux_df.columns and col != "anon_id":
            q_ids.append(col)

    #take take anon_df, merge with aux_df from left using q_ids
    match_frame = anon_df.merge(aux_df, on=q_ids, how="left")

    #Adding a count of number of matches using groupby
    match_frame["match_count"] = match_frame.groupby("anon_id")["name"].transform("count")
    #using only unique matches, so we do matches where the count = 1
    matches = match_frame[match_frame["match_count"] == 1]
    #We get our unique pairs by taking our matches two columns of anond_id and name, we also rename the name to matched_name
    pairs = matches[["anon_id", "name"]].rename(columns={"name": "matched_name"})

    return pairs
    


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)
 
