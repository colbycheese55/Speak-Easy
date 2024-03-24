import customtkinter as ctk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import perplexity
import sentiment_analysis
#import perspect
from perspective import Attributes

satoshiFont = ("Satoshi", 24)
satoshiBold = ("Satoshi", 24, "bold")
satoshiBoldSmall = ("Satoshi", 20, "bold")
satoshiLight = ("Satoshi", 20, "italic")


root = ctk.CTk()
root.title("HooHacks24")
previousChats = list()
previousChatsBtns = list()

root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=2)
root.columnconfigure(3, weight=1)

ctk.set_default_color_theme("dark-blue")

# Left Panel
leftPanel = ctk.CTkFrame(root, width=300, height=700)
leftPanel.grid(row=1, rowspan=10, column=1, columnspan=1, padx=40, pady=40, sticky="n")

historyLabel = ctk.CTkLabel(leftPanel, text="Chat History", font=satoshiBold, width=300)
historyLabel.grid(row=1, rowspan=1, sticky="n")

for i in range(10):
    btn = ctk.CTkButton(leftPanel, width=200, height=40, font=("Courier New", 16), text=f"", state="disabled", fg_color="transparent")
    btn.grid(row=i+2, pady=15)
    previousChatsBtns.append(btn)
spacer = ctk.CTkLabel(leftPanel, height=80, text="")
spacer.grid(row=12)

def updateChatListing() -> None:
    for i in range(len(previousChats)):
        cmd = lambda text=previousChats[i][1]: printOutput(text, True, True)
        previousChatsBtns[i].configure(state="normal", text=previousChats[i][0], command=cmd, fg_color="yellow", text_color="black")
    if len(previousChats) >= 10:
        previousChats.pop()



# Right Panel
rightPanel = ctk.CTkFrame(root, width=300, height=700)
rightPanel.grid(row=1, rowspan=10, column=3, columnspan=1, padx=40, pady=40)

labelOut = ctk.CTkLabel(rightPanel, text="Output Language", font=("Franklin Gothic Heavy", 24), pady=10)
labelOut.grid(row=3, sticky="n")
comboboxOut = ctk.CTkComboBox(rightPanel, state="readonly", values=["Arabic", "Chinese", "English", "French", "German", "Italian", "Japanesse", "Korean", "Portuguese", "Russian", "Spanish", "Tagalog", "Vietnamese"])
comboboxOut.set("English")
comboboxOut.grid(row=4, rowspan=1, sticky="n", pady=20)

spacer = ctk.CTkLabel(rightPanel, text="", width=300, height=700)
spacer.grid(row=5, rowspan=1)

# Middle Panel
entry = ctk.CTkTextbox(root, width=700, height=80, wrap="word", font=satoshiLight)
entry.grid(row=1, rowspan=1, column=2, columnspan=1, sticky="n", pady=40)
entry.insert(ctk.END, "What do you want to translate today?")
def startEntry(*_) -> None:
    entry.delete("1.0", ctk.END)
    entry.configure(font=("Courier New", 16))
    entry.unbind("<Button-1>")
entry.bind("<Button-1>", startEntry)

def processInput(*_) -> None:
    label = ctk.CTkLabel(root, width=400, height=20, text="Output", pady=20, font=satoshiBold)
    label.grid(row=3, rowspan=1, column=2, columnspan=1)
    output.grid(row=4, rowspan=4, column=2, columnspan=1)

    input = entry.get("1.0", ctk.END).replace("\n", "")
    #attributes = sentimentAnalysis(input)
    emotions = sentiment_analysis.ibm_analysis(input)
    sentiment = {
        "Sentiment Score": "{:.2f}%".format(sentiment_analysis.sentiment_analysis(input)*100),
    }
    emotion = {
        "Sadness": "{:.2f}%".format(emotions["sadness"]*100),
        "Joy": "{:.2f}%".format(emotions["joy"]*100),
        "Fear": "{:.2f}%".format(emotions["fear"]*100),
        "Disgust": "{:.2f}%".format(emotions["disgust"]*100),
        "Anger": "{:.2f}%".format(emotions["anger"]*100)
    }
    sentiment = "\n".join([f"{key}: {sentiment[key]}" for key in sentiment])
    emotion = "\n".join([f"{key}: {emotion[key]}" for key in emotion])

    language = comboboxOut.get()
    summary = perplexity.make_perplexity_call(language, input)
    rerun = 0
    while(rerun < 20 and len(summary) < 2):
        summary = perplexity.make_perplexity_call(language, input)
        rerun += 1
        
    out = f"Sentiment Analysis: \n{sentiment} \n{emotion} \n{summary[0]}\n\nLonger Description: \n{summary[1]}"
    printOutput(out, True)
    previousChats.insert(0, (f"{input[:10]}...", out))
    updateChatListing()

entry.bind("<Return>", processInput)

enterBtn = ctk.CTkButton(root, width = 200, height=40, text="Translate!", command=processInput, font=satoshiBold)
enterBtn.grid(row=2, rowspan=1, column=2, columnspan=1, sticky="n")

output = ctk.CTkTextbox(root, width=700, height=600, font=("Courier New", 20), wrap="word")
def printOutput(text: str, clear: bool, immediate=False) -> None:
    if clear:
        output.delete("1.0", ctk.END)
    short_text, long_text = text.split("\n\nLonger Description: \n", 1)
    def insert_text(i, text):
        if not immediate:
            if i < len(text):
                output.insert(ctk.END, text[i])
                root.after(5, insert_text, i+1, text)
        else:
            output.insert(ctk.END, text)
    insert_text(0, short_text)

    def show_long_text():
        output.delete("1.0", ctk.END)
        insert_text(0, "Longer Description: \n" + long_text)
        btn.configure(text="Show Less", command=show_short_text, font=satoshiBoldSmall)  # Change the button text and command

    def show_short_text():
        output.delete("1.0", ctk.END)
        insert_text(0, short_text)
        btn.configure(text="Show More", command=show_long_text, font=satoshiBoldSmall)  # Change the button text and command back

    btn = ctk.CTkButton(root, text="Show More", command=show_long_text, font=satoshiBoldSmall)
    btn.grid(row=8, rowspan=1, column=2, columnspan=1, sticky="n", pady=20)  # Added pady=20


root.bind("<Control-w>", lambda _: root.destroy())


if __name__ == "__main__":
    root.mainloop()


