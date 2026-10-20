from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]

def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def pdf(path, title, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [title, "MEDORBIT EDUCATION RESOURCE", ""]
    for paragraph in body:
        lines += textwrap.wrap(paragraph, 88) + [""]
    lines += [
        "Verify current eligibility, fees, deadlines and rules with the relevant official authority.",
        "This is an informational guide, not an official notice or guarantee of admission/employment."
    ]
    chunks = [lines[i:i+48] for i in range(0, len(lines), 48)] or [[]]
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [" + " ".join(f"{4+i*2} 0 R" for i in range(len(chunks))) + f"] /Count {len(chunks)} >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    ]
    for i, chunk in enumerate(chunks):
        pageid = 4 + i*2
        stream = ["BT", "/F1 10 Tf", "48 790 Td", "14 TL"]
        for line in chunk:
            stream += [f"({esc(line[:105])}) Tj", "T*"]
        stream += ["ET"]
        raw = "\n".join(stream).encode("latin-1", "replace")
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {pageid+1} 0 R >>")
        objs.append(f"<< /Length {len(raw)} >>\nstream\n{raw.decode('latin-1')}\nendstream")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, obj in enumerate(objs, 1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n{obj}\nendobj\n".encode("latin-1"))
    xref = len(out)
    out.extend(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode())
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode())
    out.extend(f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    path.write_bytes(out)

guides = [
("engineering/engineering-admission-guide.pdf","Engineering Admission Guide",[
"Compare approved institutions, programme accreditation, degree title, curriculum, labs, placements and total cost.",
"Check the official AICTE portal and the institution/university for current approval and affiliation details.",
"Confirm the relevant entrance route and counselling process: requirements vary by institution, state and programme.",
"Review tuition, hostel, transport, examination fees, refund rules and scholarship eligibility before accepting a seat."
]),
("general-education/higher-education-checklist.pdf","Higher Education Planning Checklist",[
"Choose the qualification level, subject, study mode, location and expected career outcome.",
"Check eligibility, recognized awarding body, programme duration, accreditation where relevant and total cost.",
"Confirm application dates and required documents using the institution's official notice.",
"Compare several options and keep a copy of applications, receipts, allotment letters and official correspondence."
]),
("admissions/scholarship-application-guide.pdf","Scholarship Application Guide",[
"Search official national, state, institution and research-fellowship portals.",
"Check income limits, academic conditions, category rules, renewal requirements and application dates.",
"Prepare only the documents explicitly required by the scholarship authority.",
"Never pay a fee to an unofficial agent who promises guaranteed scholarship approval."
]),
("jobs/job-application-checklist.pdf","Job Application and Recruitment Checklist",[
"Use the employer's official recruitment notification to verify post, eligibility, age rules, pay scale, selection process and deadlines.",
"Check whether the notification has been amended, extended, cancelled or superseded before applying.",
"Submit applications only through the specified official portal and retain the application number and payment receipt.",
"Do not treat a general job-source link as a confirmed vacancy. This checklist is not a live job advertisement.",
"Never pay unofficial agents for guaranteed government employment."
]),
("nmc/medical-admission-checklist.pdf","Medical Admission Checklist",[
"Check the current NMC information and applicable counselling authority for course, college recognition and seat details.",
"Review entrance exam eligibility, registration, counselling rounds, seat matrix and deadlines for the relevant academic year.",
"Verify fee category, bond/service rules, hostel costs and required original documents with the institution and counselling authority.",
"Recognition, seat permission and admissions can change. Confirm the current official record before making a decision."
])
]

for rel, title, body in guides:
    path = ROOT / "public/pdfs" / rel
    pdf(path, title, body)
    print("CREATED", path)
