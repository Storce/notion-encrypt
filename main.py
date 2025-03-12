import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your Notion integration token and parent page ID.
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")  # e.g., "secret_..."
PARENT_PAGE_ID = os.environ.get("PARENT_PAGE_ID")  # The parent page acting as your "document"
CHILD_PAGE_ID = os.environ.get("CHILD_PAGE_ID")  # The child page acting as your "document"
print(NOTION_TOKEN)
print(PARENT_PAGE_ID)
print(CHILD_PAGE_ID)

# Initialize the Notion client.
notion = Client(auth=NOTION_TOKEN)

def get_child_pages(parent_id):
    """
    Retrieve all child pages (blocks of type "child_page") of the given parent page.
    """
    pages = []
    next_cursor = None
    while True:
        response = notion.blocks.children.list(
            block_id=parent_id,
            start_cursor=next_cursor
        )
        for block in response.get("results"):
            if block.get("type") == "child_page":
                pages.append(block)
        if not response.get("has_more"):
            break
        next_cursor = response.get("next_cursor")
    return pages

def process_page(page_id: str):
    next_cursor = None
    while True:
        response = notion.blocks.children.list(
            block_id=page_id,
            start_cursor=next_cursor
        )
        for block in response.get("results"):
            processed_block = process_block(block)
            print(processed_block)
        if not response.get("has_more"):
            break
        next_cursor = response.get("next_cursor")
    return None

def process_block(block: dict):
    if block.get("type") == "paragraph":
        paragraph = block.get("paragraph")
        if "rich_text" in paragraph and isinstance(paragraph["rich_text"], list):
            for text_obj in block["rich_text"]:
                # Check if the block element is of type 'text' and has a 'text' dict.
                if text_obj.get("type") == "text" and "text" in text_obj:
                    text_obj["text"]["content"] = "hello world"
                    text_obj["plain_text"] = "hello world"    
    return block

def main():
    process_page(CHILD_PAGE_ID)

if __name__ == "__main__":
    main()
