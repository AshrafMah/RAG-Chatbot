import typer
import os

import re

from haystack import Document
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter

from swift.WeaviateIngestion.fetch_github import (
    fetch_docs,
    download_file,
    is_link_working,
)
from swift.WeaviateIngestion.util import hash_string

from wasabi import msg  # type: ignore[import]
from dotenv import load_dotenv

load_dotenv()


def retrieve_documentation() -> tuple[list[Document], list[Document]]:
    """Downloads the Weaviate documentation, preprocesses, and chunks it. Returns a list of full documents and a list of chunks
    @returns tuple[list[Document], list[Document]] - A tuple of list of documents and list of chunks
    """
    weaviate_documentation = download_from_github(
        "weaviate",
        "weaviate-io",
        "developers/",
        os.environ.get("GITHUB_TOKEN", ""),
        "Documentation",
    )

    chunked_weaviate_documentation = chunking_data(weaviate_documentation)

    return weaviate_documentation, chunked_weaviate_documentation


def retrieve_blogs() -> tuple[list[Document], list[Document]]:
    """Downloads the Weaviate documentation, preprocesses, and chunks it. Returns a list of full documents and a list of chunks
    @returns tuple[list[Document], list[Document]] - A tuple of list of documents and list of chunks
    """
    weaviate_documentation = download_from_github(
        "weaviate",
        "weaviate-io",
        "blog/",
        os.environ.get("GITHUB_TOKEN", ""),
        "Blog",
    )

    chunked_weaviate_documentation = chunking_data(weaviate_documentation)

    return weaviate_documentation, chunked_weaviate_documentation


def download_from_github(
    owner: str,
    repo: str,
    folder_path: str,
    token: str = None,
    doc_type: str = "Documentation",
) -> list[Document]:
    """Downloads .mdx/.md files from Github
    @parameter owner : str - Repo owner
    @parameter repo : str - Repo name
    @parameter folder_path : str - Directory in repo to fetch from
    @parameter token : str - Github token
    @parameter doc_type : str - Document type (code, blogpost, podcast)
    @returns list[Document] - A list of haystack documents
    """
    msg.divider(f"Starting downloading {doc_type} from {owner}/{repo}/{folder_path}")
    document_names = fetch_docs(owner, repo, folder_path, token)
    raw_docs = []
    for document_name in document_names:
        try:
            fetched_text, link, path = download_file(owner, repo, document_name, token)
        except Exception as e:
            msg.fail(str(e))

        if filtering(path, doc_type):
            doc = Document(
                content=cleaning(fetched_text, doc_type),
                meta={
                    "doc_name": process_filename(str(path), doc_type),
                    "doc_hash": hash_string(str(path)),
                    "doc_type": doc_type,
                    "doc_link": process_url(str(path), doc_type, fetched_text),
                },
            )
            msg.info(f"Loaded {doc.meta['doc_name']}")
            raw_docs.append(doc)

    msg.good(f"All {len(raw_docs)} files successfully loaded")

    return raw_docs


# Chunking


def chunking_data(
    raw_docs: list[Document],
    split_by: str = "word",
    split_length: int = 200,
    split_overlap: int = 100,
) -> list[Document]:
    """Splits a list of docs into smaller chunks
    @parameter raw_docs : list[Document] - List of docs
    @parameter split_by : str - Chunk by words, sentences, or paragrapggs
    @parameter split_length : int - Chunk length (words, sentences, paragraphs)
    @parameter split_overlap : int - Overlapping words, sentences, paragraphs
    @returns list[Document] - List of splitted docs
    """
    msg.info("Starting splitting process")

    # Performs basic cleaning (DocumentCleaner component)
    cleaner = DocumentCleaner(
        remove_empty_lines=False,
        remove_extra_whitespaces=False,
        remove_repeated_substrings=False,
    )
    cleaned_docs = cleaner.run(documents=raw_docs)["documents"]

    # Splitter the text by performing splits and adding metadata to the text (DocumentSplitter component)
    splitter = DocumentSplitter(
        split_by=split_by,
        split_length=split_length,
        split_overlap=split_overlap,
    )
    chunked_docs = splitter.run(documents=cleaned_docs)["documents"]

    # Add split_id to each chunk
    for doc in chunked_docs:
        for i, chunk in enumerate(doc.content.split('. ')):
            doc.meta['_split_id'] = i + 1

    msg.good(f"Successful splitting (total {len(chunked_docs)})")
    return chunked_docs


# Data Filtering
def filtering(document_path: str, document_type: str) -> bool:
    """Filters documents based on their path and document type
    @parameter document_path : str - Document Path
    @parameter document_type : str - Document Type
    @returns bool - Flag whether they should be included or not
    """
    if document_type == "Documentation" or document_type == "Blog":
        return document_filtering(document_path)
    else:
        return True


def document_filtering(document_path: str) -> bool:
    """Filters documents based on their path tailored towards Weaviate documentation .md files
    @parameter document_path : str - Document Path
    @returns bool - Flag whether they should be included or not
    """
    # Split the document path into its components
    components = document_path.split("/")
    # Check if any component starts with '_'
    for component in components:
        if component.startswith("_"):
            msg.warn(f"Skipping {document_path}")
            return False
    return True


# Cleaning


def cleaning(document_str: str, document_type: str) -> str:
    """Preprocess and clean documents from mdx markings
    @parameter document_str : str - Document text
    @parameter document_type : str - Document Type
    @returns str - The preprocessed and cleaned document text
    """

    if document_type == "Documentation" or document_type == "Blog":
        return document_cleaning(document_str)

    return document_str


def document_cleaning(document_str: str) -> str:
    """Preprocess and clean documents from mdx markings tailored towards Weaviate documentation .md files
    @parameter document_str : str - Document text
    @returns str - The preprocessed and cleaned document text
    """
    # Step 0: Remove everything between the starting '---' pair
    text = re.sub(r"^---.*?---\n?", "", document_str, flags=re.DOTALL)

    # Step 1: Remove everything above <!-- truncate -->
    text = re.sub(r"(?s)^.*?<!-- truncate -->\n?", "", text)

    # Step 2: Remove import statements
    text = re.sub(r"import .*?;\n?", "", text)

    # Remove all HTML-like tags
    text = re.sub(r"<[^>]+>", "", text)

    # Step 4: Remove tags with three double dots and their corresponding closing tags
    text = re.sub(r":::.*?\n", "", text)
    text = re.sub(r":::\n?", "", text)

    # Step 5: Replace markdown image and link references with their text
    text = re.sub(r"!\[(.*?)\]\(.*?\)", r"\1", text)  # Image links
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)  # Normal links

    return text


# Filename Processing


def process_filename(file_path: str, document_type: str) -> str:
    """Preprocess filename based on file path and document type
    @parameter document_str : str - Document text
    @parameter document_type : str - Document Type
    @returns str - The preprocessed filename
    """
    if document_type == "Documentation" or document_type == "Blog":
        return document_process_filename(file_path)
    else:
        return file_path


def document_process_filename(file_path: str) -> str:
    """Preprocess filename based on file path and document type tailored towards Weaviate Documentation
    @parameter file_path : str - Document path
    @returns str - The preprocessed filename
    """
    # Split the path into its components
    parts = file_path.split(os.sep)

    # Check if there are at least two parts to extract
    if len(parts) < 2:
        return None

    # Remove the file extension from the last part
    filename_without_extension = os.path.splitext(parts[-1])[0]

    # If the filename is "index", use the third last and second last parts
    if filename_without_extension == "index":
        base_name = parts[-2]
        prefix = parts[-3] if len(parts) >= 3 else ""
    else:
        base_name = filename_without_extension
        prefix = parts[-2]

    # Clean the prefix and base name
    prefix = re.sub(r"^\d+_", "", prefix)
    prefix = re.sub(r"\d{4}-\d{2}-\d{2}-", "", prefix)
    base_name = re.sub(r"^\d+_", "", base_name)
    base_name = re.sub(r"\d{4}-\d{2}-\d{2}-", "", base_name)

    return "-".join([prefix, base_name]) if prefix else base_name


# URL Processing


def process_url(file_path: str, document_type: str, document_text: str = "") -> str:
    """Preprocess filename to a URL based on document type, also checks whether the link is valid
    @parameter document_str : str - Document text
    @parameter document_type : str - Document Type
    @returns str - A valid url linking to the document
    """
    processed_url = ""

    if document_type == "Documentation":
        processed_url = document_process_url(file_path)
    elif document_type == "Blog":
        processed_url = blog_process_url(document_text)
    else:
        base_url = "https://weaviate.io/"

        # Remove the file extension
        without_extension = os.path.splitext(file_path)[0]

        # Concatenate the base_url with the modified path
        full_url = os.path.join(base_url, without_extension)

        processed_url = full_url

    if not is_link_working(processed_url):
        msg.warn(f"{processed_url} not working!")

    return processed_url


def document_process_url(file_path: str) -> str:
    """Preprocess filename to a URL based on document type tailored towards Weaviate Documentation .md files
    @parameter document_str : str - Document text
    @returns str - A valid url linking to the document
    """
    base_url = "https://weaviate.io/"

    # Remove the file extension
    without_extension = os.path.splitext(file_path)[0]

    # Break down the path into individual components
    components = without_extension.split(os.sep)

    # Process each component
    for i, component in enumerate(components):
        # Remove leading numbers and underscores
        while component and (component[0].isdigit() or component[0] == "_"):
            component = component[1:]
        components[i] = component

    # Join the modified components
    modified_path = os.sep.join(components)

    # Concatenate the base_url with the modified path
    full_url = os.path.join(base_url, modified_path)

    # Remove trailing "/index"
    if full_url.endswith("/index"):
        full_url = full_url[:-6]

    return full_url


def blog_process_url(document_text: str) -> str:
    """Preprocess filename to a URL based on document type tailored towards Weaviate Blog .md files
    @parameter document_str : str - Document text
    @returns str - A valid url linking to the document
    """
    base_url = "https://weaviate.io/blog/"

    def extract_slug(text: str) -> str:
        """Extract slug content from the provided text."""
        match = re.search(r"slug:\s*(\S+)", text)
        return match.group(1) if match else None

    slug = extract_slug(document_text)

    full_url = base_url + slug

    return full_url