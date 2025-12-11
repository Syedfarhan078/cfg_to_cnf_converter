Chomsky Normal Form (CNF) Converter – Flask Web App

An interactive web application that converts any user-defined Context-Free Grammar (CFG) into Chomsky Normal Form (CNF) while clearly displaying each transformation step.
Built using Python, Flask, HTML, CSS, and a clean UI for easy grammar visualization.


🚀 Features

✔ User-friendly interface to enter and parse grammars

✔ Step-by-step CNF transformation

ε-elimination

Unit production removal

Long rule reduction

Terminal replacement

✔ Readable and structured output formatting

✔ Flask-powered web backend

✔ Clean and responsive HTML/CSS front-end

✔ Lightweight and easy to deploy on any system

📂 Project Structure
/static
    └── style.css
/templates
    └── index.html
app.py
README.md

🛠️ Installation & Setup

Install Python 3

Install dependencies:

pip install flask


Run the application:

python app.py


Open the browser and visit:

http://127.0.0.1:5000

📘 How It Works

The app follows the standard formal steps used in CNF conversion:

Remove nullable productions

Remove unit productions

Reduce rules to binary form

Replace terminals in complex rules

These steps are based on the standard CNF definitions from reputable sources:

CNF Grammar Reference (GeeksforGeeks): https://www.geeksforgeeks.org/chomsky-normal-form

Formal Language Theory (TutorialsPoint): https://www.tutorialspoint.com/automata_theory/chomsky_normal_form.htm

Flask Framework Official Documentation: https://flask.palletsprojects.com

📸 Demo Output

Parsed Grammar

After ε-Elimination

After Unit Production Removal

After Long Rule Splitting

Final CNF Form

Each step is displayed neatly inside a modern card-style box.
<img width="736" height="890" alt="Screenshot 2025-12-11 133939" src="https://github.com/user-attachments/assets/4119cf0d-71d0-45ef-be3a-b732ab8b77d3" />

<img width="577" height="894" alt="image" src="https://github.com/user-attachments/assets/52bffcff-efe4-43a9-9126-8ec8a30ef480" />


🤝 Contributing

Pull requests and improvements are welcome.
If you'd like to add themes, animations, or support for more grammar formats—feel free to contribute!
