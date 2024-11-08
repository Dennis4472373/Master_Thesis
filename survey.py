import pandas as pd
import sys


def question_entry(df, argv):

    num = int(argv[1])

    with open("survey_questions.txt", "w") as file:
        file.write('[[AdvancedFormat]]\n\n')

        for row in df.synthetic.sample(num):
            file.write(f'[[Question:TextEntry]]\n{row}\n\n')


def slider(df):
    with open("survey_questions.txt", "w") as file:
        file.write('[[AdvancedFormat]]\n\n')

        for index, row in df.iterrows():
            file.write(f'[[Question:Matrix]]\n{row.Source}\n\n[[Choices]]\n{row.Gen_comp}\n{row.Gen_comp1}\n{row.Gen_comp2}\n[[AdvancedAnswers]]\n[[Answer]]\n1\n[[Answer]]\n2\n[[Answer]]\n3\n[[Answer]]\n4\n[[Answer]]\n5\n\n[[PageBreak]]\n\n')


def main(argv):

    df = pd.read_csv('filtered_similarity.csv')
    
    # question_entry(df, argv)
    slider(df)

if __name__ == "__main__":
    main(sys.argv)