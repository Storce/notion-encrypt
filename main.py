import os
from notion_client import Client
from dotenv import load_dotenv
import encrypt

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

def get_child_pages(parent_id: str) -> list:
    """
    Retrieve all child page ids of the given parent page.
    """
    pages = []
    next_cursor = None
    response = notion.blocks.children.list(
            block_id=parent_id
    )
    for block in response.get("results"):
        if block.get("type") == "child_page":
            pages.append(block.get("id"))
    return pages


def get_all_blocks(page_id: str) -> list:
    """
    Retrieve all blocks of a given page.
    """
    blocks = []
    next_cursor = None
    response = notion.blocks.children.list(
        block_id=page_id
    )
    for block in response.get("results"):
        blocks.append(block)
    return blocks


def process_block(blocks: list) -> list:
    """
    Process and encrypt a list of blocks. Return the modified list.
    """
    for block in blocks:
        if block.get("type") == "paragraph":
            paragraph = block.get("paragraph")
            for content in paragraph["rich_text"]:
                encrypted_text = encrypt.encrypt(content['text']['content'])
                content['text']['content'] = encrypted_text
                content['plain_text'] = encrypted_text

    return blocks


def get_title(page_id: str) -> str:
    """
    Retrieve the title of a page.
    """
    response = notion.pages.retrieve(page_id=page_id)
    return response.get("properties").get("title").get("title")[0].get("text").get("content")


def create_page(blocks: list, parent_id: str, title: str) -> bool:
    """
    Create a new page with the given blocks under the specified parent.
    """
    new_page = notion.pages.create(
        parent={"type": "page_id", "page_id": parent_id},
        children=blocks,
        properties={"title": {"title": [{"type": "text", "text": {"content": "gib." + title}}]}},
    )
    return True


def main():
    for page_id in get_child_pages(PARENT_PAGE_ID):
        processed = process_block(get_all_blocks(page_id))
        create_page(processed, PARENT_PAGE_ID, get_title(page_id))

if __name__ == "__main__":
    main()
