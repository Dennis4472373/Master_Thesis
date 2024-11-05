import pandas as pd
import evaluate
from tqdm import tqdm


def compare_generations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compate the generation sentences with each other
    using ChrF score and remove rows where score is lower than 70
    Args:
        df (DataFrame): The dataframe including generated sentences
    Returns:
        Dictionary: The filtered dataframe
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
    filtered_df = compare_generations(filtered_df)

    filtered_df.to_csv('filtered_similarity.csv')


if __name__ == "__main__":
    main()
