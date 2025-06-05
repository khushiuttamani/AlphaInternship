import pandas as pd

# reading the existing casv file
def run_quiz_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    #Initialize the Score Counter
    score = 0
    total_questions = len(df)

    print("\n🎓 Welcome to the Quiz Game!\n")

    for idx, row in df.iterrows(): #index of each row in the dataset
        question = row['Question']
        correct_answer = str(row['Answer']).strip().lower()
        category = row['Category']

        print(f"Q{idx+1}: {question}  (Category: {category})")
        user_answer = input("Your Answer: ").strip().lower() #strip() and lower() so comparisons are not affected

        if user_answer == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {row['Answer']}\n")

    print("Quiz Complete!")
    print(f"Your Score: {score} / {total_questions} ({(score / total_questions) * 100:.2f}%)")

    if score == total_questions:
        print("Perfect! You nailed it!")
    elif score >= total_questions * 0.75:
        print("Great job!")
    elif score >= total_questions * 0.5:
        print("Good try. Keep practicing!")
    else:
        print("Don't worry, try again and you'll improve!")

if __name__ == "__main__":
    run_quiz_from_csv('1_quiz/quiz_data.csv')  # Make sure this file exists
