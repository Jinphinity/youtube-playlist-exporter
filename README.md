# YouTube Playlist Transcript Exporter

This tool consolidates transcripts from a YouTube playlist into a single Markdown file with collapsible sections for each video. It is designed to facilitate converting video content into study notes or textual archives.

## Features
- **Consolidated Output**: Generates one Markdown file containing transcripts for all videos in a playlist.
- **Collapsible Sections**: Each video's transcript is wrapped in a `<details>` tag for clean navigation.
- **Smart Chunking**: Groups captions into readable paragraphs based on time gaps or character limits.
- **Timestamps**: Optional support for timestamped lines.
- **Reformatting**: Can re-parse its own output to change formatting styles without re-fetching data.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd youtube-playlist-exporter
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Basic Usage
Fetch transcripts for a playlist and save to `playlist_transcript.md` (default):

```bash
python main.py "https://www.youtube.com/playlist?list=PL..."
```

### Advanced Options

-   **Specify Output File**:
    ```bash
    python main.py "https://www.youtube.com/playlist?list=PL..." --out "my_course_notes.md"
    ```

-   **Include Timestamps**:
    ```bash
    python main.py "https://www.youtube.com/playlist?list=PL..." --timestamps
    ```

-   **Change Style** (bullet points instead of paragraphs):
    ```bash
    python main.py "https://www.youtube.com/playlist?list=PL..." --style bullet
    ```

-   **Reformat Existing File** (no internet needed):
    ```bash
    python main.py --from-markdown "old_notes.md" --style bullet --out "new_notes.md"
    ```

### Command Line Arguments
-   `playlist_url`: The URL of the YouTube playlist (required unless `--from-markdown` is used).
-   `--out`: Output filename (default: `playlist_transcript.md`).
-   `--timestamps`: Add `[MM:SS]` timestamps to each chunk.
-   `--style`: Choose between `paragraph` (default) or `bullet`.
-   `--max-gap-seconds`: Max seconds of silence before starting a new paragraph (default: 30.0).
-   `--max-chars`: Max characters per paragraph (default: 500).
-   `--languages`: Language codes to prefer (default: `en`).

## Suggested Workflow for Study Notes

This tool is part of a workflow to convert video courses into study material:

1.  **Export**: Run this tool to get the raw verbatim transcripts.
    ```bash
    python main.py "PLAYLIST_URL" --out raw_transcripts.md
    ```
2.  **Process**: Use an LLM or manual review to summarize the content. The collapsible structure makes it easy to process one video at a time.
    -   *Tip*: Keep the original transcript in the `<details>` block and write your summary above or below it.

## Testing

Run the included tests to ensure everything is working:

```bash
python -m unittest tests.py
```
