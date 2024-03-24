import customtkinter as ctk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

import perplexity
import sentiment_analysis
from perspective import Attributes
from perspect import analyze_text

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
    btn = ctk.CTkButton(leftPanel, width=200, height=40, font=("Courier New", 16), text=f"", state="disabled",
                        fg_color="transparent")
    btn.grid(row=i + 2, pady=15)
    previousChatsBtns.append(btn)
spacer = ctk.CTkLabel(leftPanel, height=80, text="")
spacer.grid(row=12)


def updateChatListing() -> None:
    for i in range(len(previousChats)):
        cmd = lambda text=previousChats[i][1]: printOutput(text, True, True)
        previousChatsBtns[i].configure(state="normal", text=previousChats[i][0], command=cmd, fg_color="yellow",
                                       text_color="black")
    if len(previousChats) >= 10:
        previousChats.pop()


# Right Panel
rightPanel = ctk.CTkFrame(root, width=300, height=700)
rightPanel.grid(row=1, rowspan=10, column=3, columnspan=1, padx=40, pady=40, sticky="ns")

# Language Selection Frame
languageFrame = ctk.CTkFrame(master=rightPanel)
languageFrame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

labelOut = ctk.CTkLabel(languageFrame, text="Output Language", font=("Franklin Gothic Heavy", 24), pady=10)
# Add padding around the label
labelOut.grid(row=0, sticky="n", padx=20, pady=10)
comboboxOut = ctk.CTkComboBox(languageFrame, state="readonly",
                              values=["Arabic", "Chinese", "English", "French", "German", "Italian", "Japanese",
                                      "Korean", "Portuguese", "Russian", "Spanish", "Tagalog", "Vietnamese"])
comboboxOut.set("English")
comboboxOut.grid(row=1, sticky="n", pady=20)

# Progress Bars Frame
progressFrame = ctk.CTkFrame(master=rightPanel)
progressFrame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

# spacer = ctk.CTkLabel(rightPanel, text="", width=300, height=700)
# spacer.grid(row=5, rowspan=1)

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

    input_text = entry.get("1.0", ctk.END).replace("\n", "")
    emotions = sentiment_analysis.ibm_analysis(input_text)
    language = comboboxOut.get()
    summary = perplexity.make_perplexity_call(language, input_text)
    rerun = 0
    while rerun < 20 and len(summary) < 2:
        summary = perplexity.make_perplexity_call(language, input_text)
        rerun += 1

    out = f"{summary[0]}\n\nLonger Description: \n{summary[1]}"
    printOutput(out, True)
    previousChats.insert(0, (f"{input_text[:10]}...", out))
    updateChatListing()

    # Analyze the text
    attributes = [Attributes.TOXICITY, Attributes.INSULT, Attributes.INFLAMMATORY]
    analysis = analyze_text(input_text, attributes)

    # Progress Bars with Titles
    attribute_titles = {
        Attributes.TOXICITY: "Toxicity",
        Attributes.INSULT: "Insult",
        Attributes.INFLAMMATORY: "Inflammatory"
    }

    toxicity_widgets = []  # List to store toxicity widgets for toggling
    sentiment_widgets = []  # List to store sentiment widgets for toggling

    # Create progress bars for toxicity
    for i, attribute in enumerate(attributes):
        score = analysis[str(attribute)] / 100  # Normalize score to a value between 0 and 1

        title_label = ctk.CTkLabel(master=progressFrame, text=attribute_titles[attribute], font=("Courier New", 16))
        progressbar = ctk.CTkProgressBar(master=progressFrame, width=200, height=20)
        progressbar.set(score)

        toxicity_widgets.extend([title_label, progressbar])

    # Create progress bars for sentiment
    emotion_scores = {
        "Sentiment": sentiment_analysis.sentiment_analysis(input_text),
        "Sadness": emotions["sadness"],
        "Joy": emotions["joy"],
        "Fear": emotions["fear"],
        "Disgust": emotions["disgust"],
        "Anger": emotions["anger"]
    }

    attribute_titles.update({
        "Sentiment": "Sentiment",
        "Sadness": "Sadness",
        "Joy": "Joy",
        "Fear": "Fear",
        "Disgust": "Disgust",
        "Anger": "Anger"
    })

    starting_row = len(attributes) * 2
    for i, (emotion, score) in enumerate(emotion_scores.items()):
        title_label = ctk.CTkLabel(master=progressFrame, text=attribute_titles[emotion], font=("Courier New", 16))
        progressbar = ctk.CTkProgressBar(master=progressFrame, width=200, height=20)
        progressbar.set(score)

        sentiment_widgets.extend([title_label, progressbar])

    # Function to toggle the visibility of toxicity progress bars
    def toggle_toxicity_bars():
        for widget in toxicity_widgets:
            widget.grid_forget() if widget.winfo_viewable() else widget.grid()

    # Function to toggle the visibility of sentiment progress bars
    def toggle_sentiment_bars():
        for widget in sentiment_widgets:
            widget.grid_forget() if widget.winfo_viewable() else widget.grid()

    # Buttons to toggle the visibility of progress bars
    toggle_toxicity_btn = ctk.CTkButton(root, text="Toxicity Analysis", command=toggle_toxicity_bars, font=satoshiBoldSmall)
    toggle_sentiment_btn = ctk.CTkButton(root, text="Sentiment Analysis", command=toggle_sentiment_bars, font=satoshiBoldSmall)

    # Place the toggle buttons next to the 'Show More' button
    toggle_toxicity_btn.grid(row=8, column=2, sticky="e", padx=10)
    toggle_sentiment_btn.grid(row=8, column=2, sticky="w", padx=10)

entry.bind("<Return>", processInput)


enterBtn = ctk.CTkButton(root, width=200, height=40, text="Translate!", command=processInput, font=satoshiBold)
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
                root.after(5, insert_text, i + 1, text)
        else:
            output.insert(ctk.END, text)

    insert_text(0, short_text)

    def show_long_text():
        output.delete("1.0", ctk.END)
        insert_text(0, "Longer Description: \n" + long_text)
        btn.configure(text="Show Less", command=show_short_text,
                      font=satoshiBoldSmall)  # Change the button text and command

    def show_short_text():
        output.delete("1.0", ctk.END)
        insert_text(0, short_text)
        btn.configure(text="Show More", command=show_long_text,
                      font=satoshiBoldSmall)  # Change the button text and command back

    btn = ctk.CTkButton(root, text="Show More", command=show_long_text, font=satoshiBoldSmall)
    btn.grid(row=8, rowspan=1, column=2, columnspan=1, sticky="n", pady=20)  # Added pady=20


root.bind("<Control-w>", lambda _: root.destroy())

if __name__ == "__main__":
    root.mainloop()


