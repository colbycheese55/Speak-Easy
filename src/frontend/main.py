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
leftPanel.grid(row=1, rowspan=10, column=1, columnspan=1, padx=40, pady=40, sticky="n")

historyLabel = ctk.CTkLabel(leftPanel, text="Chat History", font=("Franklin Gothic Heavy", 24), width=300)
historyLabel.grid(row=1, rowspan=1, sticky="n")

for i in range(10):
    btn = ctk.CTkButton(leftPanel, width=200, height=40, font=("Courier New", 16), text=f"Chat {i+1}", state="disabled")
    btn.grid(row=i+2, pady=15)
    previousChatsBtns.append(btn)

def updateChatListing() -> None:
    for i in range(len(previousChats)):
        cmd = lambda text=previousChats[i][1]: printOutput(text, True)
        previousChatsBtns[i].configure(state="normal", text=previousChats[i][0], command=cmd)
    if len(previousChats) >= 10:
        previousChats.pop()



# Right Panel
rightPanel = ctk.CTkFrame(root, width=300, height=700)
rightPanel.grid(row=1, rowspan=10, column=3, columnspan=1, padx=40, pady=40)


labelIn = ctk.CTkLabel(rightPanel, text="Input Language", font=("Franklin Gothic Heavy", 24), pady=10)
labelIn.grid(row=1, sticky="n")
comboboxIn = ctk.CTkComboBox(rightPanel, state="readonly", values=["Arabic", "Chinese", "English", "French", "German", "Italian", "Japanesse", "Korean", "Portuguese", "Russian", "Spanish", "Tagalog", "Vietnamese"])
comboboxIn.set("English")
comboboxIn.grid(row=2, rowspan=1, sticky="n", pady=20)
labelOut = ctk.CTkLabel(rightPanel, text="Output Language", font=("Franklin Gothic Heavy", 24), pady=10)
labelOut.grid(row=3, sticky="n")
comboboxOut = ctk.CTkComboBox(rightPanel, state="readonly", values=["Arabic", "Chinese", "English", "French", "German", "Italian", "Japanesse", "Korean", "Portuguese", "Russian", "Spanish", "Tagalog", "Vietnamese"])
comboboxOut.set("English")
comboboxOut.grid(row=4, rowspan=1, sticky="n", pady=20)
_ = ctk.CTkLabel(rightPanel, text="", width=300, height=500)
_.grid(row=5, rowspan=1)

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

    input = entry.get("1.0", ctk.END).replace("\n", "")
    #attributes = sentimentAnalysis(input)
    attributes = {"stuff": "things"}
    attributes = "\n".join([f"{key}: {attributes[key]}" for key in attributes])

    summary = perplexity.make_perplexity_call("english", input)
    out = f"Sentiment Analysis: \n{attributes} \n\nNatural Language Summary: \n{summary[0]}\n\nLonger Description: \n{summary[1]}"
    printOutput(out, True)
    previousChats.insert(0, (f"{input[:10]}...", out))
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


