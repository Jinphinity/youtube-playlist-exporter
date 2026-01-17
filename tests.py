import unittest
import main as pt
from pathlib import Path

class PlaylistTranscriptsFormattingTests(unittest.TestCase):
    def test_collapsible_section_with_timestamps(self):
        transcript = [
            {"start": 0.0, "text": "Hello world"},
            {"start": 7.4, "text": "Second line"},
        ]
        section = pt.build_collapsible_section(
            title="01 - Intro", transcript=transcript, include_timestamps=True
        )
        expected = (
            "<details>\n"
            "<summary>01 - Intro</summary>\n\n"
            "[00:00]–[00:07] Hello world Second line\n\n"
            "</details>\n"
        )
        self.assertEqual(section.strip(), expected.strip())

    def test_render_consolidated_marks_missing_transcript(self):
        entries = [
            {"index": 1, "title": "Intro", "transcript": [{"start": 0, "text": "Line"}]},
            {"index": 2, "title": "Missing", "transcript": None},
        ]
        rendered = pt.render_consolidated(
            entries=entries, include_timestamps=False, playlist_title="Sample Playlist"
        )
        self.assertIn("# Sample Playlist", rendered)
        self.assertIn("_no transcript available_", rendered)
        # Ensure ordering follows index with collapsible blocks per video
        expected_order = [
            "<summary>01 - Intro</summary>",
            "<summary>02 - Missing</summary>",
        ]
        for marker in expected_order:
            self.assertIn(marker, rendered)

    def test_chunking_splits_on_gap(self):
        transcript = [
            {"start": 0.0, "text": "First"},
            {"start": 10.0, "text": "Second"},
            {"start": 45.0, "text": "Third far later"},
        ]
        chunks = pt.chunk_transcript(transcript, max_gap_seconds=30, max_chars=100)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["text"], "First Second")
        self.assertEqual(chunks[1]["text"], "Third far later")

    def test_parse_existing_markdown(self):
        md = """# Sample

<details>
<summary>01 - Title</summary>

[00:00] Hello world
[00:45] Later line

</details>
"""
        tmp_path = "tmp_parse.md"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(md)
        try:
            title, entries = pt.parse_existing_markdown(Path(tmp_path))
            self.assertEqual(title, "Sample")
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["title"], "Title")
            self.assertEqual(entries[0]["transcript"][0]["text"], "Hello world")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_bullet_style_rendering(self):
        entries = [
            {
                "index": 1,
                "title": "Intro",
                "transcript": [
                    {"start": 0.0, "text": "Hello world"},
                    {"start": 12.0, "text": "More content"},
                ],
            }
        ]
        rendered = pt.render_consolidated(
            entries=entries,
            include_timestamps=True,
            playlist_title="Sample",
            style="bullet",
        )
        self.assertIn("- [00:00]–[00:12] Hello world More content", rendered)

    def test_render_video_markdown_with_date(self):
        entry = {
            "title": "My Video",
            "upload_date": "20230101",
            "transcript": [{"start": 0, "text": "Hi"}],
        }
        rendered = pt.render_video_markdown(entry, include_timestamps=False)
        self.assertIn("# My Video (20230101)", rendered)
        self.assertIn("Hi", rendered)
        self.assertNotIn("<details>", rendered)


if __name__ == "__main__":
    unittest.main()
