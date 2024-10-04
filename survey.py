import pandas as pd
import sys


def main(argv):

    num = int(argv[1])
    df = pd.read_csv('syn_data.csv')
    
    with open("survey_questions.txt", "w") as file:
        file.write('[[AdvancedFormat]]\n\n')

        for row in df.synthetic.sample(num):
            file.write(f'[[Question:TextEntry]]\n{row}\n\n')

if __name__ == "__main__":
    main(sys.argv)