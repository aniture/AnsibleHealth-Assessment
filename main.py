import re
from googleapiclient.discovery import build

def parse_markdown(markdown_text):
    lines = markdown_text.split("\n")
    parsed = []

    for line in lines:
        if line.startswith("# "):
            parsed.append(("h1", line[2:].strip()))
        elif line.startswith("## "):
            parsed.append(("h2", line[3:].strip()))
        elif line.startswith("### "):
            parsed.append(("h3", line[4:].strip()))
        elif line.strip().startswith("- [ ]"):
            text = line.strip()[5:].strip()
            text = "☐ " + text  
            parsed.append(("checkbox", text))
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            parsed.append(("bullet", line.strip()[2:].strip()))
        else:
            parsed.append(("text", line.strip()))
    return parsed

def bold_mentions(text):
    pattern = r"(@\w+)"
    return re.sub(pattern, r"**\1**", text)

def build_google_doc_requests(parsed_items):
    requests = []
    for item_type, content in parsed_items:
        content = bold_mentions(content)
        insert = {
            "insertText": {
                "location": {"index": 1},
                "text": content + "\n"
            }
        }
        requests.append(insert)

        if item_type == "h1":
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(content)},
                    "paragraphStyle": {"namedStyleType": "HEADING_1"},
                    "fields": "namedStyleType"
                }
            })
        elif item_type == "h2":
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(content)},
                    "paragraphStyle": {"namedStyleType": "HEADING_2"},
                    "fields": "namedStyleType"
                }
            })
        elif item_type == "h3":
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(content)},
                    "paragraphStyle": {"namedStyleType": "HEADING_3"},
                    "fields": "namedStyleType"
                }
            })
        elif item_type in ("bullet", "checkbox"):
            requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": 1, "endIndex": 1 + len(content)},
                    "bulletPreset": "BULLET_CHECKBOX"
                }
            })
    return requests

def create_google_doc(service, title, parsed_items):
    doc = service.documents().create(body={"title": title}).execute()
    doc_id = doc.get("documentId")

    requests = build_google_doc_requests(parsed_items)

    try:
        service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests}
        ).execute()
        print("Document created successfully:", doc_id)
    except Exception as e:
        print("Error updating document:", e)

    return doc_id

if __name__ == "__main__":
    import sample_notes

    with open("sample_notes.md", "r") as f:
        markdown_text = f.read()

    parsed = parse_markdown(markdown_text)

    from google.colab import auth
    auth.authenticate_user()

    service = build("docs", "v1")

    create_google_doc(service, "Product Team Sync - Converted", parsed)
