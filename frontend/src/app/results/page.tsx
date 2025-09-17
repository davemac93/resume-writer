"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "../../components/ui/button";
import { Textarea } from "../../components/ui/textarea";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

export default function ResultsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [resume, setResume] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const resumeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Get resume data from URL params or localStorage
    const resumeData = searchParams.get('resume') || localStorage.getItem('generatedResume');
    if (resumeData) {
      try {
        // Only decode if it's from URL params (which would be encoded)
        const decodedData = searchParams.get('resume') 
          ? decodeURIComponent(resumeData) 
          : resumeData; // localStorage data is already decoded
        setResume(decodedData);
        setIsLoading(false);
      } catch (error) {
        console.error('Error decoding resume data:', error);
        // If decoding fails, use the raw data
        setResume(resumeData);
        setIsLoading(false);
      }
    } else {
      // If no resume data, redirect back to home
      router.push('/');
    }
  }, [searchParams, router]);

  const handleDownloadPDF = async () => {
    if (!resumeRef.current) return;
    
    try {
      // Show loading state
      const originalContent = resumeRef.current.innerHTML;
      resumeRef.current.innerHTML = '<div style="text-align: center; padding: 50px; font-size: 16px; color: #666;">Generating PDF...</div>';
      
      const canvas = await html2canvas(resumeRef.current, {
        scale: 3, // Higher scale for better quality
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        width: resumeRef.current.scrollWidth,
        height: resumeRef.current.scrollHeight,
        windowWidth: 1200,
        windowHeight: 1600
      });
      
      // Restore original content
      resumeRef.current.innerHTML = originalContent;
      
      const imgData = canvas.toDataURL('image/png', 1.0);
      const pdf = new jsPDF('p', 'mm', 'a4');
      const imgWidth = 210; // A4 width in mm
      const pageHeight = 297; // A4 height in mm
      const margin = 10; // 10mm margin
      const contentWidth = imgWidth - (margin * 2);
      const imgHeight = (canvas.height * contentWidth) / canvas.width;
      
      let heightLeft = imgHeight;
      let position = margin;
      
      // Add first page
      pdf.addImage(imgData, 'PNG', margin, position, contentWidth, imgHeight);
      heightLeft -= (pageHeight - margin * 2);
      
      // Add additional pages if needed
      while (heightLeft >= 0) {
        position = heightLeft - imgHeight + margin;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', margin, position, contentWidth, imgHeight);
        heightLeft -= (pageHeight - margin * 2);
      }
      
      pdf.save('generated-resume.pdf');
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error generating PDF. Please try again.');
    }
  };

  const handleDownloadTXT = () => {
    if (!resume) return;
    
    const blob = new Blob([resume], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated-resume.txt';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleCopyMarkdown = async () => {
    if (!resume) return;
    
    try {
      // Convert plain text to markdown format
      const markdownResume = convertToMarkdown(resume);
      await navigator.clipboard.writeText(markdownResume);
      alert('Resume copied to clipboard in Markdown format!');
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

      const formatResumeForPDF = (text: string): string => {
        // Parse the resume text and create a professional HTML structure
        const lines = text.split('\n');
        let html = '';
        let currentSection = '';
        
        // Extract name and title from the first few lines
        const name = lines[0] || 'Resume';
        const title = lines[1] || '';
        
        html = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8" />
          <title>${name} - Resume</title>
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <style>
            @page {
              size: A4;
              margin: 16mm 14mm 16mm 14mm;
            }
            * { 
              box-sizing: border-box; 
              margin: 0;
              padding: 0;
            }
            body {
              font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
              color: #111827;
              font-size: 11pt;
              line-height: 1.35;
              -webkit-print-color-adjust: exact;
              print-color-adjust: exact;
              margin: 0;
              padding: 0;
              background: white;
            }
            .container {
              max-width: 780px;
              margin: 0 auto;
              padding: 0;
            }
            .header {
              padding-bottom: 8px;
              border-bottom: 1px solid #e5e7eb;
              margin-bottom: 10px;
            }
            .name {
              font-size: 20pt;
              font-weight: 800;
              color: #0f172a;
              letter-spacing: 0.1px;
              margin-bottom: 4px;
            }
            .title {
              font-size: 11pt;
              color: #2563eb;
              font-weight: 600;
              margin-bottom: 6px;
            }
            .contact {
              font-size: 9.8pt;
              color: #6b7280;
              margin-bottom: 8px;
            }
            .skills {
              display: flex;
              flex-wrap: wrap;
              gap: 4px;
              margin-bottom: 8px;
            }
            .skill-tag {
              background: #eef2ff;
              color: #111827;
              padding: 2px 8px;
              border-radius: 12px;
              font-size: 9pt;
              font-weight: 500;
            }
            .section-title {
              font-weight: 800;
              color: #0f172a;
              font-size: 12pt;
              margin-top: 14px;
              margin-bottom: 6px;
              letter-spacing: 0.1px;
              text-transform: uppercase;
            }
            .section {
              margin-bottom: 6px;
            }
            .entry {
              margin-bottom: 10px;
              break-inside: avoid;
            }
            .entry-head {
              display: flex;
              justify-content: space-between;
              align-items: baseline;
              margin-bottom: 4px;
            }
            .entry-title {
              font-weight: 700;
              color: #0f172a;
              font-size: 11pt;
            }
            .company {
              color: #6b7280;
              font-weight: 600;
              font-size: 11pt;
            }
            .dates {
              color: #6b7280;
              font-size: 10pt;
              white-space: nowrap;
            }
            .bullets {
              margin: 4px 0 4px 18px;
              padding: 0;
            }
            .bullets li {
              margin: 2px 0;
              font-size: 10pt;
              line-height: 1.3;
            }
            .summary {
              margin-top: 6px;
              font-size: 10pt;
              line-height: 1.4;
            }
            .divider {
              height: 1px;
              background: #e5e7eb;
              margin: 8px 0;
            }
            .key-impact {
              font-weight: 700;
              color: #0f172a;
              margin-top: 6px;
              margin-bottom: 4px;
            }
            .key-impact-bullets {
              margin: 4px 0 4px 18px;
              padding: 0;
            }
            .key-impact-bullets li {
              margin: 2px 0;
              font-size: 10pt;
              line-height: 1.3;
            }
            ul {
              margin-block-start: 0.4em;
              margin-block-end: 0.4em;
            }
            li {
              list-style-type: disc;
            }
            .key-impact-bullets li {
              list-style-type: disc;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <header class="header">
              <div class="name">${name}</div>
              <div class="title">${title}</div>
              <div class="contact">
                Lodz, Poland • Email: dawid.mac@hotmail.com • Phone: 502 109 666 • 
                LinkedIn: https://www.linkedin.com/in/dawid-maciejewski-32668289/ • 
                GitHub: https://github.com/davemac93
              </div>
              <div class="skills">
                <span class="skill-tag">Data Analysis</span>
                <span class="skill-tag">Data Management</span>
                <span class="skill-tag">Master Data</span>
                <span class="skill-tag">Process Optimization</span>
                <span class="skill-tag">SQL</span>
                <span class="skill-tag">Power BI</span>
                <span class="skill-tag">Python</span>
                <span class="skill-tag">UiPath</span>
                <span class="skill-tag">SAP</span>
                <span class="skill-tag">Ariba</span>
                <span class="skill-tag">ServiceNow</span>
              </div>
            </header>
            <main>`;
        
        // Process the rest of the content
        let inList = false;
        let currentList = '';
        let inKeyImpact = false;
        let keyImpactList = '';
        
        for (let i = 2; i < lines.length; i++) {
          const line = lines[i].trim();
          
          if (!line) continue;
          
          // Check for section headers
          if (line.match(/^[A-Z][A-Z\s]{3,}$/) || 
              line.match(/^(SUMMARY|EXPERIENCE|EDUCATION|SKILLS|PROJECTS|CERTIFICATIONS|CONTACT|OBJECTIVE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE):?$/i)) {
            
            if (inList) {
              html += `<ul class="bullets">${currentList}</ul>`;
              inList = false;
              currentList = '';
            }
            if (inKeyImpact) {
              html += `<ul class="key-impact-bullets">${keyImpactList}</ul>`;
              inKeyImpact = false;
              keyImpactList = '';
            }
            
            const sectionName = line.replace(/:/g, '').toUpperCase();
            html += `<section class="section">
              <div class="section-title">${sectionName}</div>`;
            currentSection = sectionName;
          }
          // Check for "Key impact" sub-section
          else if (line.match(/^Key impact$/i)) {
            if (inList) {
              html += `<ul class="bullets">${currentList}</ul>`;
              inList = false;
              currentList = '';
            }
            html += `<div class="key-impact">Key impact</div>`;
            inKeyImpact = true;
            keyImpactList = '';
          }
          // Check for bullet points
          else if (line.match(/^[\s]*[-•]\s*(.+)$/) || line.match(/^[\s]*\d+\.\s*(.+)$/)) {
            if (!inList && !inKeyImpact) {
              inList = true;
              currentList = '';
            }
            const content = line.replace(/^[\s]*[-•\d+\.]\s*/, '');
            if (inKeyImpact) {
              keyImpactList += `<li>${content}</li>`;
            } else {
              currentList += `<li>${content}</li>`;
            }
          }
          // Regular content
          else {
            if (inList) {
              html += `<ul class="bullets">${currentList}</ul>`;
              inList = false;
              currentList = '';
            }
            if (inKeyImpact) {
              html += `<ul class="key-impact-bullets">${keyImpactList}</ul>`;
              inKeyImpact = false;
              keyImpactList = '';
            }
            
            if (currentSection === 'SUMMARY') {
              html += `<div class="summary">${line}</div>`;
            } else {
              html += `<div>${line}</div>`;
            }
          }
        }
        
        // Close any remaining lists
        if (inList) {
          html += `<ul class="bullets">${currentList}</ul>`;
        }
        if (inKeyImpact) {
          html += `<ul class="key-impact-bullets">${keyImpactList}</ul>`;
        }
        
        // Close sections
        html += `</section>
            </main>
          </div>
        </body>
        </html>`;
        
        return html;
      };

  const convertToMarkdown = (text: string): string => {
    // Convert plain text resume to markdown format
    let markdown = text
      // Convert headers (lines that are all caps or start with specific patterns)
      .replace(/^([A-Z][A-Z\s]+)$/gm, '# $1')
      .replace(/^([A-Z][a-z\s]+:)$/gm, '## $1')
      // Convert bullet points
      .replace(/^[\s]*[-•]\s*(.+)$/gm, '- $1')
      .replace(/^[\s]*\d+\.\s*(.+)$/gm, '$1. $1')
      // Convert email addresses
      .replace(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g, '[$1](mailto:$1)')
      // Convert phone numbers
      .replace(/(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})/g, '**$1**')
      // Convert URLs
      .replace(/(https?:\/\/[^\s]+)/g, '[$1]($1)')
      // Add line breaks for better formatting
      .replace(/\n\n/g, '\n\n')
      // Bold important sections
      .replace(/^(Experience|Education|Skills|Projects|Contact|Summary|Objective):/gm, '**$1:**');
    
    return markdown;
  };

  const handleGenerateNew = () => {
    localStorage.removeItem('generatedResume');
    router.push('/');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen relative">
        {/* Header */}
        <header className="fixed top-0 left-0 right-0 z-50 header-blur">
          <div className="max-w-7xl mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div className="text-2xl font-bold text-white">soleil noir</div>
              <nav className="flex items-center space-x-1 glass-card rounded-full px-6 py-3">
                <a href="/" className="text-sm font-medium text-white hover:text-blue-400 transition-colors relative">
                  <span className="w-2 h-2 bg-blue-500 rounded-full absolute -left-4 top-1/2 transform -translate-y-1/2"></span>
                  home
                </a>
                <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                  projects
                </a>
                <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                  about us
                </a>
                <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                  contact
                </a>
              </nav>
            </div>
          </div>
        </header>

        {/* Loading State */}
        <main className="pt-32 pb-20 px-6">
          <div className="max-w-6xl mx-auto">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-white/70">Loading your resume...</p>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 header-blur">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="text-2xl font-bold text-white">soleil noir</div>
            <nav className="flex items-center space-x-1 glass-card rounded-full px-6 py-3">
              <a href="/" className="text-sm font-medium text-white hover:text-blue-400 transition-colors relative">
                <span className="w-2 h-2 bg-blue-500 rounded-full absolute -left-4 top-1/2 transform -translate-y-1/2"></span>
                home
              </a>
              <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                projects
              </a>
              <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                about us
              </a>
              <a href="#" className="text-sm font-medium text-white/70 hover:text-white transition-colors ml-6">
                contact
              </a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-32 pb-20 px-6">
        <div className="max-w-6xl mx-auto">
          {/* Success Header */}
          <div className="text-center mb-12">
            <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
              resume
              <br />
              <span className="text-blue-400">generated</span>
            </h1>
            <p className="text-xl text-white/70 max-w-2xl mx-auto leading-relaxed">
              Your AI-crafted resume is ready for download and use
            </p>
          </div>

          {/* Resume Content */}
          <div className="glass-card rounded-2xl p-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-semibold text-white">Generated Resume</h2>
              <div className="flex flex-wrap gap-2">
                <Button 
                  variant="outline" 
                  onClick={handleCopyMarkdown}
                  className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-xs"
                >
                  Copy MD
                </Button>
                <Button 
                  variant="outline" 
                  onClick={handleDownloadTXT}
                  className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-xs"
                >
                  Download TXT
                </Button>
                <Button 
                  onClick={handleDownloadPDF}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-xs"
                >
                  Download PDF
                </Button>
                <Button 
                  variant="outline" 
                  onClick={handleGenerateNew}
                  className="bg-white/10 border-white/20 text-white hover:bg-white/20 text-xs"
                >
                  Generate New
                </Button>
              </div>
            </div>
            
                {/* Resume display for PDF generation */}
                <div 
                  ref={resumeRef}
                  className="bg-white text-black rounded-lg mb-4 overflow-hidden"
                  style={{ 
                    minHeight: '1000px',
                    fontFamily: 'Inter, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
                    lineHeight: '1.35',
                    fontSize: '11pt',
                    color: '#111827',
                    padding: '0',
                    margin: '0',
                    width: '100%'
                  }}
                >
                  <div 
                    dangerouslySetInnerHTML={{
                      __html: formatResumeForPDF(resume)
                    }}
                    style={{
                      width: '100%',
                      height: '100%'
                    }}
                  />
                </div>
            
            {/* Editable textarea for viewing */}
            <Textarea 
              value={resume} 
              readOnly 
              rows={15} 
              className="w-full font-mono text-sm leading-relaxed resize-none border-0 bg-white/5 text-white placeholder:text-white/50 focus:ring-0 focus:outline-none rounded-lg p-6"
            />
          </div>

          {/* Action Buttons */}
          <div className="text-center mt-12">
            <Button 
              onClick={handleGenerateNew}
              variant="outline"
              className="bg-white/10 border-white/20 text-white hover:bg-white/20 px-8 py-3"
            >
              Generate Another Resume
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
