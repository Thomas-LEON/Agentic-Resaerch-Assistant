import os
import requests
import argparse
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

def search_arxiv(topic, max_results=5):
    """
    Searches for papers on arXiv based on a topic.
    """
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    response = requests.get(url, params=params)
    return response.text

def parse_arxiv_data(xml_data):
    """
    Parses the XML data from the arXiv API.
    """
    root = ET.fromstring(xml_data)
    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        papers.append({"title": title, "summary": summary})
    return papers

def generate_report(topic, papers):
    """
    Generates a simple Markdown report.
    """
    report = f"# Research Report on {topic}\n\n"
    report += "## arXiv Papers\n\n"
    for paper in papers:
        report += f"### {paper['title']}\n\n"
        report += f"{paper['summary']}\n\n"
    return report

def main():
    """
    Main function to run the research agent.
    """
    parser = argparse.ArgumentParser(description="A simple research agent.")
    parser.add_argument("topic", help="The research topic.")
    args = parser.parse_args()

    print(f"Generating report for topic: {args.topic}")
    arxiv_data = search_arxiv(args.topic)
    papers = parse_arxiv_data(arxiv_data)
    report = generate_report(args.topic, papers)

    with open(f"report_{args.topic.replace(' ', '_')}.md", "w") as f:
        f.write(report)

    print("Report generated successfully.")

if __name__ == "__main__":
    main()
