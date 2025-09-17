from datetime import date
from pathlib import Path
from playwright.sync_api import sync_playwright

resume = {
  "name": "Dawid Maciejewski",
  "title": "IT Analyst | Data Warehouse & Analytics",
  "tags": [
    "Data Analysis",
    "Data Modeling",
    "Data Warehousing",
    "SQL",
    "ETL",
    "BI",
    "Cloud Databases",
    "Requirements Management"
  ],
  "location": "Warszawa, Poland",
  "email": "dawid.mac@hotmail.com",
  "phone": "502 109 666",
  "linkedin": "https://www.linkedin.com/in/dawid-maciejewski-32668289/",
  "github": "https://github.com/davemac93",
  "summary": "IT Analyst with a Computer Science degree and a passion for data analysis and problem-solving. While I do not have the required 5 years of experience, I have over 3 years of experience in IT-facing roles, with a proven track record of translating business requirements into IT specifications and performing complex data analysis. I have hands-on experience with SQL, ETL/BI processes, and working with multinational virtual teams. I am a fast learner with a strong desire to expand my knowledge of Data Warehousing industry standards and modern cloud technologies like Snowflake. I am confident that my analytical skills, proactive attitude, and collaborative mindset will allow me to quickly bridge any knowledge gaps and contribute effectively to the Common Data Warehouse Requirements and Analysis team.",
  "core_skills": {
    "Data Analysis & Modeling": "Complex data analysis, translating business requirements into IT mappings, understanding data patterns, BI/Data Analytics, experience with SQL for data extraction and analysis",
    "Requirements & Project Management": "Requirements management, clarifying requirements for IT, acting as an interface between business and IT, Agile/Scrum methodologies",
    "Data Architecture & Tools": "Understanding of ETL/BI/Data Analytics/Data Modelling processes, experience with cloud-based databases, Power BI, JSON, Python scripting",
    "Communication & Soft Skills": "Excellent interpersonal communications, proficiency in English and Polish, experience in multinational virtual teams, collaborative mindset, proactive and problem-solving attitude"
  },
  "experience": [
    {
      "role": "Digital Specialist (IT Analyst)",
      "company": "Danfoss",
      "dates": "2025-03 – Present",
      "bullets": [
        "Performed complex data analysis to clarify requirements and test use cases for digital solutions.",
        "Mapped business needs to IT specifications for data platforms and automated solutions.",
        "Acted as a technical SME for data transformation projects, helping data engineers understand the requirements and data patterns.",
        "Worked with multinational teams across various geographies to deliver data-driven solutions."
      ],
      "impact": [
        "Led the development of a real-time Power BI dashboard, performing hands-on data analysis to ensure its functionality met business needs.",
        "Successfully managed and executed multiple digitalization projects, demonstrating a strong understanding of data-driven solutions."
      ]
    },
    {
      "role": "Procurement Specialist (IT Project Coordinator)",
      "company": "Danfoss",
      "dates": "2024-04 – 2025-03",
      "bullets": [
        "Gathered and analyzed data requirements from multi-regional stakeholders, acting as an interface between business and IT.",
        "Translated business needs into actionable IT solutions, showcasing a strong understanding of requirements management.",
        "Used Python scripting and SQL concepts for SAP data extraction, demonstrating experience with data integration and analysis."
      ],
      "impact": [
        "Coordinated the implementation of automated solutions that reduced the invoice backlog by 60%, showing the ability to perform complex data analysis for process improvement."
      ]
    },
    {
      "role": "Service and Solution Delivery Specialist",
      "company": "Philips",
      "dates": "2021-07 – 2024-03",
      "bullets": [
        "Assisted in the implementation and testing of the Ariba procurement module, working with development teams to ensure requirements were met.",
        "Piloted automation scripts in ServiceNow, demonstrating a proactive approach and a curiosity to go beyond my own domain.",
        "Prepared work instructions and documentation, showcasing an ability to clarify and present complex information."
      ],
      "impact": [
        "Contributed to the successful go-live of a large-scale project, working within a multinational virtual team to ensure a smooth transition."
      ]
    }
  ],
  "projects": [
    {
      "name": "Procurement Analytics Control Tower",
      "stack": "Power BI, SQL, SAP",
      "desc": [
        "Designed data models, defined KPIs, and managed the project to provide a centralized view of procurement operations. This project showcases proficiency in data analysis and translating business needs into a functional data-driven solution, directly aligning with the role's responsibilities."
      ]
    },
    {
      "name": "PO and FO Automation for SAP System",
      "stack": "Python, SAP",
      "desc": [
        "Coordinated a project to automate the processing of orders in SAP, demonstrating direct experience with ETL-like processes and working with an ERP system."
      ]
    }
  ],
  "education": [
    {
      "name": "Bachelor’s Degree in Computer Science, University of Lodz",
      "dates": "2021-09 – 2024-06"
    }
  ],
  "certifications": [
    "Google Data Analytics Professional Certificate (2024)",
    "Google AI Essentials (2024)",
    "SAP Technology Consultant — In Progress"
  ],
  "strengths": [
    "**Experience:** While I have over 3 years of experience in IT, I do not meet the 5-year requirement. However, my diverse project experience and Bachelor's degree in Computer Science provide a strong foundation for the role.",
    "**Passion & Mindset:** I have a genuine passion for data analysis, problem-solving, and a continuous learning mindset, which aligns with Nordea’s culture of learning and development.",
    "**Technical Skills:** I possess hands-on experience in writing SQL and have a solid understanding of ETL/BI/Data Analytics processes from my previous roles, making me well-equipped to quickly adapt to the technology stack.",
    "**Collaboration:** I have extensive experience working in multinational virtual teams and acting as an interface between business and IT, a key requirement for the role."
  ],
  "additional": [
    "Work model: Hybrid (Location: Warszawa)",
    "Fluent in English and Polish (local language)."
  ],
  "fit": [
    "**Background:** Possesses a degree in Computer Science or a related field.",
    "**Experience:** While I do not have 5 years of experience, I have over 3 years in IT, with relevant experience in requirements management and working in multinational virtual teams.",
    "**Skills:** Has hands-on experience in writing SQL, understands ETL/BI/Data Analytics/Data Modelling processes, and is fluent in English.",
    "**Mindset:** I have a passion for data analysis and problem-solving and am known for my proactive and collaborative mindset.",
    "**GDPR Clause for Poland:** 'In accordance with art. 6 (1) a and b. Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation) hereinafter ‘GDPR’. I agree to have: my personal data, education and employment history proceeded for the purposes of current and future recruitment processes in Nordea Bank Abp. The administrator of your personal data is: Nordea Bank Abp operating in Poland through its Branch, address: Aleja Edwarda Rydza Śmiglego 20, 93-281 Łodź. Your personal data will be processed for the recruitment processes in Nordea Bank Abp. You have a right to access your personal data, right to rectify and right to delete. Disclosing the personal data in the scope specified by the provisions of Polish Labour Code from 26 June 1974 and executive acts are mandatory. Providing personal data is necessary to conduct the recruitment processes. The request for the deletion of your personal data means resignation from further participation in recruitment processes and causes the immediate removal of your application. Detailed information concerning processing of your personal data can be found at: https://www.nordea.com/en/doc/nordea-privacy-policy-for-applicants.pdf'"
  ]
}


def render_html(d):
  primary = "#0f172a"  # slate-900
  accent = "#2563eb"   # blue-600
  text = "#111827"     # gray-900 for better print contrast
  subtle = "#6b7280"   # gray-500
  border = "#e5e7eb"   # gray-200
  bgchip = "#eef2ff"   # indigo-50 (softer)
  hair = "#f3f4f6"     # gray-100 divider

  tag_html = "".join(f'<span class="chip">{t}</span>' for t in d["tags"])

  core_skills_html = "".join(
      f'<div class="skill-row"><span class="skill-key">{k}</span><span class="skill-sep"> · </span><span class="skill-val">{v}</span></div>'
      for k, v in d["core_skills"].items()
  )

  exp_html = ""
  for e in d["experience"]:
    bullets = "".join(f"<li>{b}</li>" for b in e["bullets"])
    impact = "".join(f"<li>{i}</li>" for i in e["impact"])
    exp_html += f"""
      <section class="entry">
        <div class="entry-head">
          <div class="entry-title">{e['role']} <span class="at">·</span> <span class="company">{e['company']}</span></div>
          <div class="dates">{e['dates']}</div>
        </div>
        <ul class="bullets">{bullets}</ul>
        <div class="subhead">Key impact</div>
        <ul class="bullets">{impact}</ul>
      </section>
    """

  proj_html = ""
  for p in d["projects"]:
    desc = "".join(f"<li>{x}</li>" for x in p["desc"])
    proj_html += f"""
      <section class="entry">
        <div class="entry-head">
          <div class="entry-title">{p['name']} <span class="stack">— {p['stack']}</span></div>
        </div>
        <ul class="bullets">{desc}</ul>
      </section>
    """

  edu_html = "".join(
    f"""
      <div class='edu-item'>
        <div class="edu-line">{e['name']}</div>
        <div class='edu-dates'>{e['dates']}</div>
      </div>
    """
    for e in d["education"]
  )

  cert_html = "".join(f"<li>{c}</li>" for c in d["certifications"])
  strengths_html = "".join(f"<li>{s}</li>" for s in d["strengths"])
  additional_html = "".join(f"<li>{a}</li>" for a in d["additional"])
  fit_html = "".join(f"<li>{f}</li>" for f in d["fit"])

  year = date.today().year

  html = f"""
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="utf-8" />
      <title>{d['name']} - Resume</title>
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <style>
        @page {{
          size: A4;
          margin: 16mm 14mm 16mm 14mm;
        }}
        :root {{
          --primary: {primary};
          --accent: {accent};
          --text: {text};
          --subtle: {subtle};
          --border: {border};
          --bgchip: {bgchip};
          --hair: {hair};
        }}
        * {{ box-sizing: border-box; }}
        body {{
          font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          color: var(--text);
          font-size: 11pt;
          line-height: 1.35;
          -webkit-print-color-adjust: exact;
          print-color-adjust: exact;
        }}
        .container {{
          max-width: 780px;
          margin: 0 auto;
        }}

        /* Header */
        .header {{
          padding-bottom: 8px;
          border-bottom: 1px solid var(--hair);
          margin-bottom: 10px;
        }}
        .name {{
          font-size: 20pt;
          font-weight: 800;
          color: var(--primary);
          letter-spacing: 0.1px;
        }}
        .title {{
          font-size: 11pt;
          color: var(--accent);
          font-weight: 600;
          margin-top: 2px;
        }}

        /* Contact directly under name/title */
        .contact-inline {{
          margin-top: 6px;
          font-size: 9.8pt;
          color: var(--subtle);
        }}
        .contact-row {{
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
        }}
        .contact-row a {{
          color: var(--subtle);
          text-decoration: none;
        }}
        .contact-row a:hover {{
          color: var(--accent);
          text-decoration: underline;
        }}
        .dot {{ color: var(--subtle); }}

        /* Tags */
        .tags {{ margin-top: 6px; }}
        .chip {{
          display: inline-block;
          background: var(--bgchip);
          color: var(--accent);
          border: 1px solid #e0e7ff;
          padding: 2px 6px;
          margin: 3px 6px 0 0;
          border-radius: 6px;
          font-size: 9pt;
          font-weight: 600;
          white-space: nowrap;
        }}

        /* Section headings */
        .section-title {{
          font-weight: 800;
          color: var(--primary);
          font-size: 12pt;
          margin-top: 14px;
          margin-bottom: 6px;
          letter-spacing: 0.1px;
        }}

        /* Content */
        .summary {{ margin-top: 6px; }}
        .section {{ margin-bottom: 6px; }}

        .entry {{ margin-bottom: 10px; break-inside: avoid; }}
        .entry-head {{
          display: grid;
          grid-template-columns: 1fr auto;
          align-items: baseline;
          gap: 8px;
        }}
        .entry-title {{
          font-weight: 700;
          color: var(--primary);
        }}
        .company {{
          color: var(--subtle);
          font-weight: 600;
        }}
        .at {{ color: var(--subtle); }}
        .dates {{ color: var(--subtle); font-size: 10pt; white-space: nowrap; }}
        .stack {{ color: var(--subtle); font-weight: 600; }}

        .subhead {{
          margin-top: 4px;
          font-weight: 700;
          color: var(--primary);
        }}

        .bullets {{ margin: 4px 0 4px 18px; padding: 0; }}
        .bullets li {{ margin: 2px 0; }}

        .skill-row {{ margin: 2px 0; break-inside: avoid; }}
        .skill-key {{ font-weight: 600; color: var(--primary); }}
        .skill-sep {{ color: var(--subtle); padding: 0 4px; }}
        .skill-val {{ color: var(--text); }}

        .edu-item {{
          display: grid;
          grid-template-columns: 1fr auto;
          padding: 2px 0;
          margin: 2px 0;
          break-inside: avoid;
        }}
        .edu-line {{ font-weight: 600; color: var(--primary); }}
        .edu-dates {{ color: var(--subtle); }}

        /* Keep blocks together near page boundaries */
        .entry, .edu-item, .skill-row {{ break-inside: avoid; }}

        /* Minimal links */
        a {{ color: inherit; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}

        /* Reduce visual noise of lists */
        ul {{ margin-block-start: 0.4em; margin-block-end: 0.4em; }}

        /* Fine hairline separators for large sections */
        .divider {{
          height: 1px;
          background: var(--hair);
          margin: 8px 0;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <header class="header">
          <div class="name">{d['name']}</div>
          <div class="title">{d['title']}</div>

          <div class="contact-inline">
            <div class="contact-row">
              <span>{d['location']}</span>
              <span class="dot">•</span>
              <span>Email: {d['email']}</span>
              <span class="dot">•</span>
              <span>Phone: {d['phone']}</span>
            </div>
            <div class="contact-row">
              <span>LinkedIn: <a href="{d['linkedin']}">{d['linkedin']}</a></span>
              <span class="dot">•</span>
              <span>GitHub: <a href="{d['github']}">{d['github']}</a></span>
            </div>
          </div>

          <div class="tags">{tag_html}</div>
        </header>

        <main>
          <section class="section">
            <div class="section-title">Summary</div>
            <div class="summary">{d['summary']}</div>
          </section>

          <div class="divider"></div>

          <section class="section">
            <div class="section-title">Experience</div>
            {exp_html}
          </section>

          <div class="divider"></div>

          <section class="section">
            <div class="section-title">Projects</div>
            {proj_html}
          </section>

          <div class="divider"></div>

          <section class="section">
            <div class="section-title">Core Skills</div>
            {core_skills_html}
          </section>

          <section class="section">
            <div class="section-title">Education</div>
            {edu_html}
          </section>

          <section class="section">
            <div class="section-title">Certifications</div>
            <ul class="bullets">{cert_html}</ul>
          </section>

          <section class="section">
            <div class="section-title">Selected Technical Strengths</div>
            <ul class="bullets">{strengths_html}</ul>
          </section>

          <section class="section">
            <div class="section-title">Additional</div>
            <ul class="bullets">{additional_html}</ul>
          </section>

          <section class="section">
            <div class="section-title">How this matches the role</div>
            <ul class="bullets">{fit_html}</ul>
          </section>
        </main>

        <footer style="margin-top:10px; color:{subtle}; font-size:9.5pt;">
          © {year} {d['name']} — Generated via Python/Chromium (Playwright)
        </footer>
      </div>
    </body>
  </html>
  """
  return html


def export_pdf(html, output_pdf="resume_dawid_maciejewski.pdf"):
  output_pdf = Path(output_pdf)
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(html, wait_until="load")
    page.pdf(
      path=str(output_pdf),
      format="A4",
      print_background=True,
      margin={"top": "16mm", "right": "14mm", "bottom": "16mm", "left": "14mm"},
    )
    browser.close()
  return str(output_pdf)


def main():
  html = render_html(resume)
  pdf_path = export_pdf(html)
  print(f"Generated: {pdf_path}")


if __name__ == "__main__":
  main()