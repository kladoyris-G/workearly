import streamlit as st
from openai import OpenAI
import json
import random

client = OpenAI(api_key="")

class Question:
    def __init__(self, question, options, correct_answer, explanation=None, image_url=None):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.image_url = image_url  # Optional: URL to an image related to the question

class Quiz:
    def __init__(self):
        self.questions = self.load_or_generate_questions()
        self.initialize_session_state()

    def load_or_generate_questions(self):
        if 'questions' not in st.session_state:
            st.session_state.questions = [
                Question("What is the capital of France?", ["London", "Paris", "Berlin", "Madrid"], "Paris",
                         "Paris is the capital and most populous city of France."),
                Question("Who developed the theory of relativity?",
                         ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Marie Curie"], "Albert Einstein",
                         "Albert Einstein is known for developing the theory of relativity, one of the two pillars of modern physics.")
            ]
        return st.session_state.questions

    def initialize_session_state(self):
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'answers_submitted' not in st.session_state:
            st.session_state.answers_submitted = 0

    def display_quiz(self):
        self.update_progress_bar()
        if st.session_state.answers_submitted >= len(self.questions):
            self.display_results()
        else:
            self.display_current_question()

    def display_current_question(self):
        question = self.questions[st.session_state.current_question_index]
        if question.image_url:
            st.image(question.image_url, width=300)  # Display image if available
        st.write(question.question)
        answer = st.radio("Choose one:", question.options, key=f"question_{st.session_state.current_question_index}")
        if st.button("Submit Answer", key=f"submit_{st.session_state.current_question_index}"):
            self.check_answer(answer)
            st.session_state.answers_submitted += 1
            if st.session_state.current_question_index < len(self.questions) - 1:
                st.session_state.current_question_index += 1
            st.rerun()

    def check_answer(self, user_answer):
        correct_answer = self.questions[st.session_state.current_question_index].correct_answer
        if user_answer == correct_answer:
            st.session_state.score += 1
            st.success("Correct answer!")
        else:
            st.error("Wrong answer!")
        if self.questions[st.session_state.current_question_index].explanation:
            st.info(self.questions[st.session_state.current_question_index].explanation)

    def display_results(self):
        st.write(f"Quiz completed! Your score: {st.session_state.score}/{len(self.questions)}")
        if st.session_state.score / len(self.questions) >= 0.8:
            st.success("Congrats! You passed the quiz!")
            st.balloons()
        else:
            st.error("You failed, try again!")
        if st.button("Restart Quiz"):
            self.restart_quiz()

    def update_progress_bar(self):
        total_questions = len(self.questions)
        progress = st.session_state.answers_submitted / total_questions
        st.progress(progress)

    def restart_quiz(self):
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.answers_submitted = 0
        st.rerun()

def generate_and_append_question(user_prompt):
    history = ""
    for q in st.session_state.questions:
        history += f"Question: {q.question} Answer: {q.correct_answer}\n"

    gpt_prompt = '''Generate a JSON response for a trivia question including the question, options, correct answer, and explanation. The format should be as follows:

{
  "Question": "The actual question text goes here?",
  "Options": ["Option1", "Option2", "Option3", "Option4"],
  "CorrectAnswer": "TheCorrectAnswer",
  "Explanation": "A detailed explanation on why the correct answer is correct.",
  "ImageURL": "Optional: URL to an image related to the question."
}'''
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": gpt_prompt},
                {"role": "user", "content": f"Create a question about: {user_prompt} that is different from those: {history}"}
            ]
        )
        gpt_response = json.loads(response.choices[0].message.content)
        new_question = Question(
            question=gpt_response["Question"],
            options=gpt_response["Options"],
            correct_answer=gpt_response["CorrectAnswer"],
            explanation=gpt_response["Explanation"],
            image_url=gpt_response.get("ImageURL")
        )
        st.session_state.questions.append(new_question)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Main app logic
if 'quiz_initialized' not in st.session_state:
    st.session_state.quiz = Quiz()
    st.session_state.quiz_initialized = True

user_input = st.text_input("Enter a topic or preference for generating a new question:")

if st.button('Generate New Question'):
    generate_and_append_question(user_input)

st.session_state.quiz.display_quiz()