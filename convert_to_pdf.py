#!/usr/bin/env python3

"""
🔥 Bug Bounty Guide PDF Converter
===============================
Converts the markdown guide to a professional PDF format
Author: Advanced Bug Bounty Hunter
Version: 1.0
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def setup_dependencies():
    """Install required dependencies if not present"""
    try:
        import markdown
        import weasyprint
        print("✅ All dependencies satisfied")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "weasyprint", "pygments"])
            return True
        except Exception as install_error:
            print(f"❌ Failed to install dependencies: {install_error}")
            return False

def create_custom_css():
    """Create custom CSS for PDF styling"""
    css_content = '''
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    @page {
        size: A4;
        margin: 2cm;
        @top-center {
            content: "Bug Bounty Hunter's Advanced Guide";
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            color: #666;
        }
        @bottom-center {
            content: counter(page) " / " counter(pages);
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            color: #666;
        }
    }
    
    body {
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        color: #2d3748;
        font-size: 11pt;
        background: white;
    }
    
    /* Headers */
    h1 {
        color: #1a202c;
        font-size: 24pt;
        font-weight: 700;
        margin: 30pt 0 20pt 0;
        padding: 15pt 0;
        border-bottom: 3pt solid #4299e1;
        page-break-before: always;
    }
    
    h1:first-child {
        page-break-before: avoid;
        text-align: center;
        color: #2b6cb0;
        font-size: 28pt;
        margin-bottom: 30pt;
    }
    
    h2 {
        color: #2d3748;
        font-size: 18pt;
        font-weight: 600;
        margin: 25pt 0 15pt 0;
        padding: 10pt 0 5pt 0;
        border-bottom: 1pt solid #e2e8f0;
    }
    
    h3 {
        color: #4a5568;
        font-size: 14pt;
        font-weight: 600;
        margin: 20pt 0 10pt 0;
    }
    
    h4 {
        color: #718096;
        font-size: 12pt;
        font-weight: 500;
        margin: 15pt 0 8pt 0;
    }
    
    /* Paragraphs */
    p {
        margin: 8pt 0;
        text-align: justify;
    }
    
    /* Lists */
    ul, ol {
        margin: 10pt 0 10pt 20pt;
    }
    
    li {
        margin: 4pt 0;
    }
    
    /* Code blocks */
    pre {
        background: #f7fafc;
        border: 1pt solid #e2e8f0;
        border-radius: 6pt;
        padding: 15pt;
        margin: 15pt 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 9pt;
        line-height: 1.4;
        overflow-x: auto;
        page-break-inside: avoid;
    }
    
    code {
        font-family: 'JetBrains Mono', monospace;
        background: #edf2f7;
        padding: 2pt 4pt;
        border-radius: 3pt;
        font-size: 10pt;
        color: #2d3748;
    }
    
    pre code {
        background: none;
        padding: 0;
        color: #2d3748;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15pt 0;
        font-size: 10pt;
    }
    
    th, td {
        border: 1pt solid #e2e8f0;
        padding: 8pt;
        text-align: left;
    }
    
    th {
        background: #f7fafc;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Blockquotes */
    blockquote {
        border-left: 4pt solid #4299e1;
        margin: 15pt 0;
        padding: 10pt 0 10pt 15pt;
        background: #f7fafc;
        font-style: italic;
    }
    
    /* Links */
    a {
        color: #3182ce;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    /* Horizontal rules */
    hr {
        border: none;
        height: 1pt;
        background: #e2e8f0;
        margin: 20pt 0;
    }
    
    /* Special boxes */
    .info-box {
        background: #ebf8ff;
        border: 1pt solid #90cdf4;
        border-radius: 6pt;
        padding: 15pt;
        margin: 15pt 0;
        page-break-inside: avoid;
    }
    
    .warning-box {
        background: #fffbeb;
        border: 1pt solid #f6e05e;
        border-radius: 6pt;
        padding: 15pt;
        margin: 15pt 0;
        page-break-inside: avoid;
    }
    
    .success-box {
        background: #f0fff4;
        border: 1pt solid #68d391;
        border-radius: 6pt;
        padding: 15pt;
        margin: 15pt 0;
        page-break-inside: avoid;
    }
    
    /* Page breaks */
    .page-break {
        page-break-before: always;
    }
    '''
    
    with open('pdf_style.css', 'w') as f:
        f.write(css_content)
    
    return 'pdf_style.css'

def markdown_to_html(markdown_file):
    """Convert markdown to HTML with extensions"""
    
    try:
        import markdown
    except ImportError:
        print("❌ Markdown not available")
        return None
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert to HTML with extensions
    html = markdown.markdown(
        markdown_content,
        extensions=[
            'toc',
            'tables', 
            'fenced_code',
            'codehilite',
            'nl2br'
        ],
        extension_configs={
            'toc': {
                'title': 'Table of Contents',
                'anchorlink': True
            },
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True
            }
        }
    )
    
    # Add proper HTML structure
    html_template = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bug Bounty Hunter's Advanced Guide</title>
        <link rel="stylesheet" href="pdf_style.css">
    </head>
    <body>
        {html}
    </body>
    </html>
    '''
    
    return html_template

def create_cover_page():
    """Create a professional cover page"""
    current_date = datetime.now().strftime('%B %Y')
    cover_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cover Page</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            body {{
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
            }}
            
            .cover-container {{
                max-width: 600px;
                padding: 40px;
            }}
            
            .title {{
                font-size: 48pt;
                font-weight: 700;
                margin-bottom: 20pt;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            
            .subtitle {{
                font-size: 24pt;
                font-weight: 400;
                margin-bottom: 40pt;
                opacity: 0.9;
            }}
            
            .description {{
                font-size: 14pt;
                line-height: 1.6;
                margin-bottom: 60pt;
                opacity: 0.8;
            }}
            
            .author {{
                font-size: 16pt;
                font-weight: 500;
                margin-bottom: 10pt;
            }}
            
            .date {{
                font-size: 12pt;
                opacity: 0.7;
            }}
            
            .icon {{
                font-size: 72pt;
                margin-bottom: 30pt;
            }}
        </style>
    </head>
    <body>
        <div class="cover-container">
            <div class="icon">🔥</div>
            <h1 class="title">Ultimate Bug Bounty Hunter's Advanced Guide</h1>
            <h2 class="subtitle">From Zero to Hero - Complete Roadmap</h2>
            <div class="description">
                একটি comprehensive guide যেটাতে সব advanced techniques এবং unique tools রয়েছে।
                Beginner থেকে Pro level পর্যন্ত সব কিছু step-by-step এবং copy-paste ready।
            </div>
            <div class="author">Created for Cybersecurity Students & Bug Bounty Hunters</div>
            <div class="date">{current_date}</div>
        </div>
    </body>
    </html>
    '''
    
    return cover_html

def html_to_pdf(html_content, output_file, css_file):
    """Convert HTML to PDF using WeasyPrint"""
    
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        print("❌ WeasyPrint not available")
        return False
    
    try:
        # Write main content to temp file
        with open('content.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("📄 Converting to PDF...")
        
        # Convert main content
        HTML('content.html', base_url='.').write_pdf(
            output_file,
            stylesheets=[CSS(css_file)]
        )
        
        print(f"✅ PDF created successfully: {output_file}")
        
        # Cleanup temp files
        if os.path.exists('content.html'):
            os.remove('content.html')
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

def main():
    """Main function to convert markdown to PDF"""
    
    parser = argparse.ArgumentParser(description='Convert Bug Bounty Guide to PDF')
    parser.add_argument('--input', '-i', default='bug_bounty_advanced_guide.md', 
                       help='Input markdown file')
    parser.add_argument('--output', '-o', default='Bug_Bounty_Advanced_Guide.pdf', 
                       help='Output PDF file')
    
    args = parser.parse_args()
    
    print("🔥 Bug Bounty Guide PDF Converter")
    print("=================================")
    
    # Setup dependencies
    if not setup_dependencies():
        return
    
    # Create CSS
    css_file = create_custom_css()
    print(f"✅ CSS created: {css_file}")
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return
    
    # Convert markdown to HTML
    print(f"📝 Converting {args.input} to HTML...")
    html_content = markdown_to_html(args.input)
    
    if html_content is None:
        print("❌ Failed to convert markdown to HTML")
        return
    
    # Convert HTML to PDF
    success = html_to_pdf(html_content, args.output, css_file)
    
    if success:
        file_size = os.path.getsize(args.output) / (1024 * 1024)  # MB
        print(f"🎉 PDF created successfully!")
        print(f"📁 File: {args.output}")
        print(f"📊 Size: {file_size:.1f} MB")
        
        # Cleanup
        if os.path.exists(css_file):
            os.remove(css_file)
            
    else:
        print("❌ PDF creation failed!")

if __name__ == "__main__":
    main()