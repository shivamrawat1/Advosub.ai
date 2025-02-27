from dotenv import load_dotenv
load_dotenv()  # This should be at the top before importing other modules
from App import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 