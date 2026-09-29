import tkinter as tk
from tkinter import scrolledtext
import re
import math
from collections import Counter
from nltk.tokenize import RegexpTokenizer


# FAQ questions and answers
faqs = [
    {
        "question": "What are your delivery charges?",
        "answer": "Delivery charges depend on your location and order."
    },
    {
        "question": "How long does delivery take?",
        "answer": "Delivery usually takes 3 to 5 working days."
    },
    {
        "question": "How can I return a product?",
        "answer": "You can request a return within 7 days of receiving your order."
    },
    {
        "question": "Can I cancel my order?",
        "answer": "Yes, you can cancel your order before it is shipped."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept UPI, debit cards, credit cards and cash on delivery."
    },
    {
        "question": "How can I track my order?",
        "answer": "You can track your order using the tracking link sent to you."
    },
    {
        "question": "Do you offer discounts?",
        "answer": "Yes, we offer discounts during special sales and promotions."
    },
    {
        "question": "How can I contact customer support?",
        "answer": "You can contact our customer support through email or phone."
    },
    {
        "question": "Is cash on delivery available?",
        "answer": "Yes, cash on delivery is available on eligible orders."
    },
    {
        "question": "What are your working hours?",
        "answer": "Our customer support is available from 9 AM to 6 PM."
    }
]


# Stop words
stop_words = {
    "is", "are", "am", "the", "a", "an", "and",
    "or", "in", "on", "at", "to", "for", "of",
    "do", "does", "can", "i", "you", "your",
    "my", "we", "our", "what", "how", "when",
    "where", "why", "who", "me", "it", "this",
    "that", "with", "from", "be", "have"
}


# Text preprocessing
def preprocess(text):
    text = text.lower()

    text = re.sub(r"[^a-z0-9\s]", "", text)

    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(text)

    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return tokens


# Cosine similarity
def cosine_similarity(text1, text2):
    words1 = preprocess(text1)
    words2 = preprocess(text2)

    if not words1 or not words2:
        return 0

    vector1 = Counter(words1)
    vector2 = Counter(words2)

    common_words = set(vector1) & set(vector2)

    dot_product = sum(
        vector1[word] * vector2[word]
        for word in common_words
    )

    magnitude1 = math.sqrt(
        sum(value ** 2 for value in vector1.values())
    )

    magnitude2 = math.sqrt(
        sum(value ** 2 for value in vector2.values())
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)


# Find matching answer
def get_answer(user_question):
    best_score = 0
    best_answer = None

    for faq in faqs:
        score = cosine_similarity(
            user_question,
            faq["question"]
        )

        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    if best_score >= 0.25:
        return best_answer

    return (
        "Sorry, I could not understand your question. "
        "Please try one of the suggested questions."
    )


# Display messages
def display_message(sender, message):
    chat_area.config(state=tk.NORMAL)

    if sender == "You":
        chat_area.insert(tk.END, "You: ", "user")
    else:
        chat_area.insert(tk.END, "Bot: ", "bot")

    chat_area.insert(tk.END, message + "\n\n")

    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)


# Send message
def send_message(event=None):
    user_question = entry_box.get().strip()

    if not user_question:
        return

    display_message("You", user_question)

    entry_box.delete(0, tk.END)

    answer = get_answer(user_question)

    display_message("Bot", answer)


# Select a suggested question
def select_question(event=None):
    selection = question_list.curselection()

    if not selection:
        return

    question = question_list.get(selection[0])

    entry_box.delete(0, tk.END)
    entry_box.insert(0, question)

    entry_box.focus()


# Double-click to send a suggested question
def send_suggested_question(event):
    select_question()
    send_message()


# Clear chat
def clear_chat():
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("1.0", tk.END)
    chat_area.config(state=tk.DISABLED)

    display_message(
        "Bot",
        "Hello! Welcome to our store. "
        "Select a suggested question or type your own."
    )


# Main window
root = tk.Tk()
root.title("FAQ Chatbot")
root.geometry("700x750")
root.resizable(False, False)
root.configure(bg="#f0f2f5")


# Heading
heading = tk.Label(
    root,
    text="General Store FAQ Chatbot",
    font=("Arial", 22, "bold"),
    bg="#f0f2f5",
    fg="#1a237e"
)
heading.pack(pady=12)


# Chat area
chat_area = scrolledtext.ScrolledText(
    root,
    width=75,
    height=17,
    font=("Arial", 11),
    wrap=tk.WORD,
    state=tk.DISABLED,
    bg="white"
)
chat_area.pack(padx=15, pady=8)


# Message colors
chat_area.tag_config(
    "user",
    foreground="blue",
    font=("Arial", 11, "bold")
)

chat_area.tag_config(
    "bot",
    foreground="green",
    font=("Arial", 11, "bold")
)


# Suggested questions heading
suggestion_label = tk.Label(
    root,
    text="Suggested Questions (Double-click to ask)",
    font=("Arial", 12, "bold"),
    bg="#f0f2f5",
    fg="#1a237e"
)
suggestion_label.pack(pady=5)


# Suggested questions list
question_list = tk.Listbox(
    root,
    width=75,
    height=5,
    font=("Arial", 10),
    bg="white",
    selectbackground="#b3d9ff",
    activestyle="dotbox"
)

question_list.pack(padx=15, pady=5)


# Add FAQ questions to list
for faq in faqs:
    question_list.insert(tk.END, faq["question"])


# Single-click to fill input
question_list.bind(
    "<<ListboxSelect>>",
    select_question
)

# Double-click to send
question_list.bind(
    "<Double-Button-1>",
    send_suggested_question
)


# Input frame
input_frame = tk.Frame(
    root,
    bg="#f0f2f5"
)
input_frame.pack(pady=10)


# Input box
entry_box = tk.Entry(
    input_frame,
    width=48,
    font=("Arial", 12)
)
entry_box.grid(row=0, column=0, padx=5)


# Send button
send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    bg="#198754",
    fg="white",
    width=10,
    command=send_message
)
send_button.grid(row=0, column=1, padx=5)


# Enter key support
entry_box.bind("<Return>", send_message)


# Clear chat button
clear_button = tk.Button(
    root,
    text="Clear Chat",
    font=("Arial", 11, "bold"),
    bg="#dc3545",
    fg="white",
    width=15,
    command=clear_chat
)
clear_button.pack(pady=5)


# Welcome message
display_message(
    "Bot",
    "Hello! Welcome to our store. "
    "Select a suggested question or type your own."
)


# Run application
root.mainloop()