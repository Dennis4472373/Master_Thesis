import json


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
            file.write(f'[[Question:Slider]]\n{row.Source}\n[[Choices]]\n{row.Gen_comp}\n{row.Gen_comp1}\n{row.Gen_comp2}\n\n[[PageBreak]]\n\n')


def main():

    file = open('test_2.qsf')
    survey = json.load(file)
    
    for item in survey['SurveyElements']:
        if item['Element'] == 'SQ':
            if 'Labels' not in item['Payload']:
                item['Payload']['Labels'] = []

    with open('better.qsf', 'w') as f:
        json.dump(survey, f)

if __name__ == "__main__":
    main()
