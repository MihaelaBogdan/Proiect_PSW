import os
import re

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff"
        "\u2600-\u26ff"
        "\u2700-\u27bf"
        "🎧📌⚙️📊🎯📈🧩🌐📐✅⚠️🔥🎵🎶📉💡🔍🧪]"
        "+", flags=re.UNICODE)
    return emoji_pattern.sub(r"", text)

files = ["app.py", "tabs/tab_overview.py", "tabs/tab_preprocessing.py", 
         "tabs/tab_statistics.py", "tabs/tab_clustering.py", 
         "tabs/tab_regression.py", "tabs/tab_classification.py", 
         "tabs/tab_advanced.py"]

for f in files:
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
        content = remove_emojis(content)
        content = content.replace("  ", " ")
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)

print("Emojies removed.")
