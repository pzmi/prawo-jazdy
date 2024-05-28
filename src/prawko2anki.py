import os
import sys
import argparse
import polars as pl

def main(input, output, category):
    outfile = open(os.path.join(output, "prawo-jazdy-pytania.txt"), "w", encoding="utf-8")

    df = pl.read_excel(input).filter(pl.col("Kategorie").is_not_null())

    for input_question in df.rows(named=True):
        categories = input_question["Kategorie"]
        if category in categories:
            try:
                question_number = input_question["Numer pytania"]
            except:
                question_number = "?"
            question = input_question["Pytanie"].replace('\n', ' ')
            answer_a = input_question["Odpowiedź A"]
            answer_b = input_question["Odpowiedź B"]
            answer_c = input_question["Odpowiedź C"]
            correct_answer = input_question["Poprawna odp"].replace('\n', ' ')
            media_file = input_question["Media"]
            # question_source = input_question["Źródło pytania"].replace('\n', ' ')
            # comment = input_question["Jaki ma związek z bezpieczeństwem"].replace('\n', ' ')

            question_html = '<div class="pytanie">' + question + '</div>'
            if media_file:
                question_html += '<div class="media">'
                if media_file.endswith(('.mp4','.wmv','.avi')):
                    question_html += '[sound:' + media_file + ']'
                elif media_file.endswith(('.jpg', '.JPG')):
                    question_html += '<img src="' + media_file + '" />'
                else:
                    raise Exception("Unexpected extension in media file: " + media_file)
                question_html +='</div>'
            if answer_a or answer_b or answer_c:
                question_html += '<div class="odpowiedzi">'
                if answer_a:
                    question_html += '<span class="wariant">A</span>: ' + answer_a + '<br>'
                if answer_b:
                    question_html += '<span class="wariant">B</span>: ' + answer_b + '<br>'
                if answer_c:
                    question_html += '<span class="wariant">C</span>: ' + answer_c + '<br>'
                question_html +='</div>'
            
            answer = '<div class="odpowiedz">'
            if correct_answer == 'Tak':
                answer += 'TAK'
            elif correct_answer == 'Nie':
                answer += 'NIE'
            elif correct_answer == 'A':
                answer += 'A: ' + answer_a
            elif correct_answer == 'B':
                answer += 'B: ' + answer_b
            elif correct_answer == 'C':
                answer += 'C: ' + answer_c
            else:
                raise Exception("Unexpected answer: " + correct_answer)
            answer += '</div>'
            
            # outfile.write(f"{question_number}\t{question_html}\t{answer}\t{comment}\t{question_source}\n")
            outfile.write(f"{question_number}\t{question_html}\t{answer}\n")

    outfile.close()
    return 0

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', 
        help='Input XLSX file name', required=True)
    parser.add_argument('-o', '--output', 
        help='Output directory', required=True)
    parser.add_argument('-c', '--category', 
        help='License category', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()

    sys.exit(main(input = args.input, output = args.output, category = args.category))

    
