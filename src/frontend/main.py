import customtkinter as ctk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import perplexity


root = ctk.CTk()
root.title("HooHacks24")
previousChats = list()
previousChatsBtns = list()

# Left Panel
leftPanel = ctk.CTkFrame(root, width=300, height=700)
leftPanel.grid(row=1, rowspan=5, column=1, columnspan=1, padx=40, pady=40, sticky="n")

historyLabel = ctk.CTkLabel(leftPanel, text="Chat History", font=("Franklin Gothic Heavy", 24), width=300)

def updateChatListing() -> None:
    if previousChatsBtns is not None:
        for btn in previousChatsBtns:
            btn.grid_forget()
    historyLabel.grid(row=1, rowspan=1, sticky="n")
    for i in range(len(previousChats)):
        cmd = lambda text=previousChats[i][1]: printOutput(text, True)
        btn = ctk.CTkButton(leftPanel, text=previousChats[i][0], font=("Courier New", 16), width = 180, height=30, command=cmd)
        btn.grid(row=(i+2), rowspan=1, sticky="n", pady=20)
        previousChatsBtns.append(btn)



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

    input = entry.get("1.0", ctk.END)
    #attributes = sentimentAnalysis(input)
    attributes = {"stuff": "things"}
    attributes = "\n".join([f"{key}: {attributes[key]}" for key in attributes])

    summary = perplexity.make_perplexity_call("english", input)
    out = f"Sentiment Analysis: \n{attributes} \n\nNatural Language Summary: \n{summary[0]}\n\nLonger Description: \n{summary[1]}"
    printOutput(out, True)
    previousChats.insert(1, (f"{input[:10]}...", out))
    updateChatListing()

entry.bind("<Return>", processInput)

enterBtn = ctk.CTkButton(root, width = 200, height=40, text="Translate!", command=processInput, font=("Franklin Gothic Heavy", 24))
enterBtn.grid(row=2, rowspan=1, column=2, columnspan=1, sticky="n")

output = ctk.CTkTextbox(root, width=400, height=600, font=("Courier New", 16), wrap="word")
def printOutput(text: str, clear: bool) -> None:
    if clear:
        output.delete("1.0", ctk.END)
    for i in range(len(text)):
        root.after(5 * i, lambda char=text[i]: output.insert(ctk.END, char))









if __name__ == "__main__":
    root.mainloop()


