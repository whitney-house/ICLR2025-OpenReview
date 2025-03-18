"""
It is a file to extract all submissions from ICLR 2025, including accept(oral/spotlight/poster),
reject, withdrawn submissions, desk rejected submissions
"""
import csv
import time
from typing import List
import openreview
from tenacity import retry, stop_after_attempt, wait_exponential
from config import USERNAME, PASSWORD
from constants import CSV_COLUMNS


class Fetcher:
    def __init__(self):
        self.client = openreview.api.OpenReviewClient(
            baseurl="https://api2.openreview.net",
            username=USERNAME,
            password=PASSWORD
        )

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30))
    def safe_get_profiles(self, author_ids: List[str]) -> List[openreview.Profile]:
        """Fetch author profiles with rate limiting and error handling"""
        try:
            batch_size = 50
            profiles = []

            for i in range(0, len(author_ids), batch_size):
                batch_ids = author_ids[i:i + batch_size]

                if i > 0:
                    time.sleep(1.5)  # Rate limiting

                batch_profiles = self.client.search_profiles(ids=batch_ids)
                profiles.extend(batch_profiles)

            return profiles
        except Exception as e:
            print(f"❌ Profile fetch failed: {str(e)}")
            raise

    def extract_institutions(self, profile: openreview.Profile) -> List[str]:
        """Extract institution names from profile history"""
        institutions = []
        history = profile.content.get("history", [])

        for entry in history:
            institution = entry.get("institution", {})
            if isinstance(institution, dict):
                name = institution.get("name", "Unknown").strip()
            else:
                name = str(institution).strip()
            if name and name != "Unknown":
                institutions.append(name)

        return institutions[-1:] if institutions else ["Unknown"]  # Latest institution only

    def fetch_papers(self, invitation: str) -> List:
        """Fetch all submissions for a given conference."""
        all_submissions = []
        chunk_size = 200
        offset = 0

        while True:
            batch = self.client.get_notes(
                invitation=invitation,
                offset=offset,
                limit=chunk_size
            )
            if not batch:
                break
            all_submissions.extend(batch)
            offset += chunk_size
            print(f"Loaded {len(all_submissions)} papers...")

        return all_submissions

    def process_papers(self, submissions: List, output_file: str):
        """Main processing pipeline"""
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_COLUMNS)

            for idx, paper in enumerate(submissions, 1):
                try:
                    # Extract basic info
                    title = paper.content.get("title", {}).get("value", "Untitled")
                    author_ids = paper.content['authorids']['value']
                    decision = paper.content.get('venue', {}).get('value', 'Unknown')

                    # Batch fetch author profiles
                    author_profiles = self.safe_get_profiles(author_ids)

                    # Process author information
                    authors = []
                    institutions = []

                    for profile in author_profiles:
                        # Author name
                        name = profile.get_preferred_name(pretty=True) if profile else "Anonymous"
                        authors.append(name)

                        # Institution data
                        inst = self.extract_institutions(profile)
                        institutions.extend(inst)

                    # Format output
                    unique_institutions = list(set(institutions))
                    author_str = ", ".join(authors)
                    institution_str = ", ".join(unique_institutions) if unique_institutions else "Unknown"

                    # Write to CSV
                    writer.writerow([title, author_str, institution_str, decision])
                    print(f"✅ Progress: {idx}/{len(submissions)} - {title[:30]}...")

                except Exception as e:
                    print(f"⚠️ Paper processing failed: {str(e)}")
                    with open("error_log.txt", "a") as logfile:
                        logfile.write(f"{time.ctime()} | Error: {str(e)}\n")


