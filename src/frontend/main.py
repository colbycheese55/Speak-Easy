import customtkinter as ctk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import perplexity


root = ctk.CTk()
root.title("HooHacks24")
previousChats = list()

# Left Panel
leftPanel = ctk.CTkFrame(root, width=300, height=700)
leftPanel.grid(row=1, rowspan=5, column=1, columnspan=1, padx=40, pady=40)


# Right Panel
rightPanel = ctk.CTkFrame(root, width=300, height=700)
rightPanel.grid(row=1, rowspan=5, column=3, columnspan=1, padx=40, pady=40)

# Middle Panel
entry = ctk.CTkTextbox(root, width=400, height=80, wrap="word", font=("Algerian", 20, "italic"))
entry.grid(row=1, rowspan=1, column=2, columnspan=1, sticky="n", pady=40)
entry.insert(ctk.END, "What do you want to translate today?")
def startEntry(*_) -> None:
    entry.delete("1.0", ctk.END)
    entry.configure(font=("Courier New", 16))
    entry.unbind("<Button-1>")
entry.bind("<Button-1>", startEntry)

def processInput(*_) -> None:
    label = ctk.CTkLabel(root, width=400, height=20, text="Output", pady=20, font=("Franklin Gothic Heavy", 24))
    label.grid(row=3, rowspan=1, column=2, columnspan=1)
    output.grid(row=4, rowspan=4, column=2, columnspan=1)
    output.delete("1.0", ctk.END)

    input = entry.get("1.0", ctk.END)
    #attributes = sentimentAnalysis(input)
    attributes = {"stuff": "things"}
    attributes = "\n".join([f"{key}: {attributes[key]}" for key in attributes])

    #summary = perplexitySummary(input)
    #summaries = perspective.make_perplexity_call("english", input)
    summary = "stuff"
    printOutput(f"Sentiment Analysis: \n{attributes} \n\nNatural Language Summary: \n{summary[0]}")

entry.bind("<Return>", processInput)

enterBtn = ctk.CTkButton(root, width = 200, height=40, text="Translate!", command=processInput, font=("Franklin Gothic Heavy", 24))
enterBtn.grid(row=2, rowspan=1, column=2, columnspan=1, sticky="n")

output = ctk.CTkTextbox(root, width=400, height=600, font=("Courier New", 16))
def printOutput(text: str) -> None:
    for i in range(len(text)):
        root.after(20 * i, lambda char=text[i]: output.insert(ctk.END, char))









if __name__ == "__main__":
    root.mainloop()


class Chat:
    def __init__(this, text: str) -> None:
        this.text = text

    def getText(this) -> str:
        return this.text