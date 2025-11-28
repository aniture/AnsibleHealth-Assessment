# Markdown → Google Docs Converter (Google Colab)

This project converts structured Markdown meeting notes into a fully formatted Google Doc using the Google Docs API.
It is designed to run inside **Google Colab** using OAuth-based user authentication.

The formatting rules match the project requirements:
- Heading 1 → Main Title
- Heading 2 → Sections (Attendees, Agenda, Action Items, etc.)
- Heading 3 → Subsections
- Nested bullet lists supported
- Markdown checkboxes (`- [ ]`) converted to Unicode checkboxes (`☐`)
- Assignee mentions (`@name`) bolded
- Footer text styled in italic and gray

## Project Structure

markdown-to-google-docs/
│── main.py
│── sample_notes.md
│── README.md
│── requirements.txt
│── .gitignore

## Setup Instructions (Colab)

1. Install dependencies:
   !pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

2. Authenticate Google API:
   from google.colab import auth
   auth.authenticate_user()

3. Run main.py or the notebook.

## License
MIT License
