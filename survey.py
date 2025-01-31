import pandas as pd


def sample_data(df, num):
    """
    Recursively sample data and create survey questions.

    Parameters:
    df (DataFrame): The input data frame.
    num (int): The current iteration number and number of survey.

    Returns:
    DataFrame: The remaining data frame after sampling.
    """

    if num > 8:
        return df

    else:
        df_elements = df.sample(n=25)

        create_questions(df_elements, num)
        df_rest = df.loc[~df.index.isin(df_elements.index)]

        return sample_data(df_rest, num+1)


def create_questions(df, num):
    """
    Create survey questions and write them to a file.

    Parameters:
    df (DataFrame): The input data frame consisting of the sampled rows.
    num (int): The number of the survey.
    """

    with open(f"Survey_questions/survey_questions_{num}.txt", "w") as file:
        file.write('[[AdvancedFormat]]\n\n')

        for index, row in df.iterrows():
            file.write(f'[[Question:Matrix]]\n{row.Source}\n\n[[Choices]]\n{row.Gen_comp}\n{row.Gen_comp1}\n{row.Gen_comp2}\n[[AdvancedAnswers]]\n[[Answer]]\n1\n[[Answer]]\n2\n[[Answer]]\n3\n[[Answer]]\n4\n[[Answer]]\n5\n\n[[PageBreak]]\n\n')


def main():

    df = pd.read_csv('Filtered_data/flan-t5-xl/filtered_similarity_flan-t5-xl_len4.csv')

    df_rest = sample_data(df, 1)

    df_rest.to_csv('Filtered_data/flan-t5-xl/rest_flan-t5-xl_len4.csv')


if __name__ == "__main__":
    main()
