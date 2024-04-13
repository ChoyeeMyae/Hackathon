from flask import Flask, request
import spacy
import sqlite3

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def process_query(query):
    """
    Processes the user's query using NLP techniques and returns relevant keywords.
    """
    doc = nlp(query)
    # Example: Extract nouns to determine the focus of the query
    nouns = [chunk.text for chunk in doc.noun_chunks]
    return nouns

@app.route('/')
def home():
    return '''
    <html>
        <body>
            <form action="/answer" method="post">
                <input type="text" name="question" placeholder="Ask a question about food security"/>
                <input type="submit"/>
            </form>
        </body>
    </html>
    '''

@app.route('/answer', methods=['POST'])
def answer():
    question = request.form['question']
    keywords = process_query(question)
    response = get_data(keywords[0] if keywords else "")  # Use the first keyword, handle no keyword case
    return f'Response: {response}'

def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_data(query_keyword):
    """
    Fetch data from the database based on a query keyword.
    """
    database = "./path/to/your/database.db"
    conn = create_connection(database)
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT answer FROM food_security WHERE keywords LIKE ?", ('%' + query_keyword + '%',))
        rows = cur.fetchall()
        conn.close()
        return rows if rows else "No data found."
    else:
        return "Database connection failed."

if __name__ == '__main__':
    app.run(debug=True)
