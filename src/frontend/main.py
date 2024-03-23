import customtkinter as ctk


root = ctk.CTk()
root.title("HooHacks24")

# Left Panel
leftPanel = ctk.CTkFrame(root, width=300, height=700)
leftPanel.grid(row=1, rowspan=5, column=1, columnspan=1, padx=40, pady=40)

# Right Panel
rightPanel = ctk.CTkFrame(root, width=300, height=700)
rightPanel.grid(row=1, rowspan=5, column=3, columnspan=1, padx=40, pady=40)

# Middle Panel
entry = ctk.CTkTextbox(root, width=400, height=80, wrap="word")
entry.grid(row=1, rowspan=1, column=2, columnspan=1, sticky="n", pady=40)
entry.insert(ctk.END, "What do you want to translate today?")
def startEntry(*_) -> None:
    entry.delete("1.0", ctk.END)
    entry.unbind("<Button-1>")
entry.bind("<Button-1>", startEntry)

output = ctk.CTkTextbox(root, width=400, height=600)
def printOutput(text: str) -> None:
    for i in range(len(text)):
        root.after(20 * i, lambda char=text[i]: output.insert(ctk.END, char))


def processInput(*_) -> None:
    label = ctk.CTkLabel(root, width=400, height=20, text="Output", pady=20)
    label.grid(row=2, rowspan=1, column=2, columnspan=1)
    output.grid(row=3, rowspan=4, column=2, columnspan=1)
    output.delete("1.0", ctk.END)

    input = entry.get("1.0", ctk.END)
    #attributes = sentimentAnalysis(input)
    attributes = {"stuff": "things"}
    attributes = "\n".join([f"{key}: {attributes[key]}" for key in attributes])

    #summary = perplexitySummary(input)
    summary = "stuff"
    printOutput(f"Sentiment Analysis: \n{attributes} \n\nNatural Language Summary: \n{summary}")

entry.bind("<Return>", processInput)






if __name__ == "__main__":
    root.mainloop()