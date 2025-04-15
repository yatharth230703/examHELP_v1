#### revision sheet page ka ek prerequisite hoga, it will only work when all flashcards have been "accessed" {bolne k liye : pehle flashcards padho fir revision karna}
# ab kya hai ki revision sheet generate krne k liye , I will generate 2 sheets: 
## 1) topic wise mindmaps, saare jitne abhi tak generate hue hai combined into one 
## 2) for the notes bhi i think the points are sufficient enough , inhe bhi directly deke as pdf print krwa lunga, ya best yahi h ki ek flashcard=pdf ka ek page
## it will be prompted to generate a sort of cheat-sheet . 

### revision_sheet.py ka simple sa kaam hai , json objects accept krega and 2 pdf release krega ,ek mindmap ka aur ek 

import json
import asyncio
import os
from jinja2 import Template
from playwright.async_api import async_playwright
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Sample list of JSON mind maps
mind_maps = [
    {
        "main_topic": "Plant Transport & Photosynthesis",
        "subtopics": [
            {
                "name": "Xylem",
                "children": [
                    "Transports water",
                    "Moves minerals",
                    "One-way flow (roots to leaves)",
                    "Made of dead cells"
                ]
            },
            {
                "name": "Phloem",
                "children": [
                    "Transports sugars",
                    "Bidirectional flow",
                    "Supports growth and storage",
                    "Made of living cells"
                ]
            },
            {
                "name": "Photosynthesis",
                "children": [
                    "Occurs in leaves",
                    "Uses sunlight, CO₂, and water",
                    "Produces glucose and oxygen",
                    "Happens in chloroplasts"
                ]
            }
        ]
    },
    {
        "main_topic": "Cell Division",
        "subtopics": [
            {
                "name": "Mitosis",
                "children": [
                    "Growth and repair",
                    "Produces identical cells",
                    "One division"
                ]
            },
            {
                "name": "Meiosis",
                "children": [
                    "Gamete production",
                    "Genetic variation",
                    "Two divisions"
                ]
            }
        ]
    }
]

# Convert JSON to Mermaid-compatible structure
def convert_to_mermaid_syntax(data):
    def format_node(text, level):
        return "  " * level + f"{text}\n"

    def build_tree(subtopics, level):
        result = ""
        for topic in subtopics:
            result += format_node(topic["name"], level)
            for child in topic.get("children", []):
                result += format_node(child, level + 1)
        return result

    root = format_node(data["main_topic"], 1)
    children = build_tree(data["subtopics"], 2)
    return f"""mindmap\n{root}{children}"""

# HTML template with heading and Mermaid block
def generate_mermaid_html(mermaid_code, title, serial_number):
    html_template = Template("""
    <html>
    <head>
        <meta charset="utf-8">
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({ startOnLoad: true });
        </script>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                margin: 2rem;
            }
            h1 {
                font-size: 1.5rem;
                margin-bottom: 1.5rem;
            }
            .mermaid {
                page-break-after: always;
            }
        </style>
    </head>
    <body>
        <h1>{{ serial_number }}. {{ title }}</h1>
        <div class="mermaid">
{{ mermaid_code }}
        </div>
    </body>
    </html>
    """)
    return html_template.render(mermaid_code=mermaid_code, title=title, serial_number=serial_number)

# Render multiple Mermaid diagrams into one PDF
async def render_multiple_mindmaps_to_pdf(mind_maps, output_pdf="combined_mindmaps.pdf"):
    temp_html_files = []

    # Step 1: Create HTML files for each mindmap
    for idx, mindmap in enumerate(mind_maps):
        mermaid_code = convert_to_mermaid_syntax(mindmap)
        html_content = generate_mermaid_html(
            mermaid_code,
            title=mindmap["main_topic"],
            serial_number=idx + 1
        )

        html_file = f"mindmap_{idx}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        temp_html_files.append(html_file)

    # Step 2: Use Playwright to generate one PDF from all HTMLs
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        pdf_pages = []

        for html_file in temp_html_files:
            page = await context.new_page()
            await page.goto(f"file://{os.path.abspath(html_file)}", wait_until="networkidle")
            pdf_pages.append(await page.pdf(format="A4", print_background=True))
            await page.close()

        # Combine all PDFs
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for idx, pdf_bytes in enumerate(pdf_pages):
            temp_path = f"temp_{idx}.pdf"
            with open(temp_path, "wb") as f:
                f.write(pdf_bytes)
            merger.append(temp_path)

        merger.write(output_pdf)
        merger.close()

        await browser.close()

    # Clean up temporary files
    for f in temp_html_files:
        os.remove(f)
    for i in range(len(pdf_pages)):
        os.remove(f"temp_{i}.pdf")

    print(f"✅ Combined PDF saved as {output_pdf}")

# Wrapper
def generate_combined_mindmaps_pdf(mind_maps, output_pdf="combined_mindmaps.pdf"):
    asyncio.run(render_multiple_mindmaps_to_pdf(mind_maps, output_pdf))


generate_combined_mindmaps_pdf(mind_maps)
    
    
   

def json_to_pdf(json_list, output_filename="output.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    for entry in json_list:
        for heading, subheadings in entry.items():
            story.append(Paragraph(f"<b>{heading}</b>", styles['Heading1']))
            story.append(Spacer(1, 12))

            for sub_heading, points in subheadings.items():
                story.append(Paragraph(f"<i>{sub_heading}</i>", styles['Heading3']))
                for point in points:
                    story.append(Paragraph(f"- {point}", styles['Normal']))
                story.append(Spacer(1, 12))

    doc.build(story)
    print(f"PDF saved as {output_filename}")

# Example usage
json_entries = [
    {
        "heading_1": {
            "sub_heading_1": ["point1", "point2", "point3"],
            "sub_heading_2": ["point1", "point2", "point3"]
        }
    },
    {
        "heading_2": {
            "sub_heading_1": ["itemA", "itemB"],
            "sub_heading_3": ["itemX"]
        }
    }
]

json_to_pdf(json_entries)