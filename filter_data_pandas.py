import pandas as pd
import evaluate
from tqdm import tqdm


def compare_generations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compate the generation sentences with each other
    using ChrF score and remove rows where score is lower than 70
    Args:
        The filtered rows where Source length > 5
    Returns:
        Dictionary: The filtered rows on total ChrF
    """

    chrf = evaluate.load('chrf')

    for index, row in tqdm(df.iterrows()):
        df.loc[index, 'Total_ChrF'] = chrf.compute(
            predictions=[row['Gen_comp'], row['Gen_comp'], row['Gen_comp1']],
            references=[[row['Gen_comp1']], [row['Gen_comp2']], [row['Gen_comp2']]])['score']
        df = df.drop(df[df['Total_ChrF'] > 70].index)

    return df


def main():

    df = pd.read_csv('Data/t5-base_cts_fine-tune_chrf.csv')

    filtered_df = df.copy()
    # filtered_df = filtered_df[filtered_df['Source'].str.split().apply(lambda x: len(x) > 5)]
    filtered_df = compare_generations(filtered_df)

    filtered_df.to_csv('Results/filtered_similarity_t5-base-test.csv')


if __name__ == "__main__":
    main()
