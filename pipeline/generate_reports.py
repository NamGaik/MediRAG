import os
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# Create output folder
# -----------------------------
os.makedirs("reports_pdf", exist_ok=True)

# -----------------------------
# Load Excel Sheets
# -----------------------------
patient_df = pd.read_excel(
    "data/Synthetic_diabetes_dataset1.xlsx",
    sheet_name="Patient_Master"
)

lab_df = pd.read_excel(
    "data/Synthetic_diabetes_dataset1.xlsx",
    sheet_name="Laboratory_Reports"
)

# -----------------------------
# Merge patient + lab data
# -----------------------------
df = lab_df.merge(
    patient_df,
    on="Patient_ID",
    how="left"
)

styles = getSampleStyleSheet()

# -----------------------------
# Clinical remarks
# -----------------------------
def get_remark(category):

    remarks = {

        "Normal":
        "All laboratory parameters are within normal clinical ranges. No evidence of impaired glucose metabolism.",

        "Prediabetic":
        "Glucose parameters are above normal limits and indicate an increased risk of progression to Type 2 Diabetes Mellitus. Lifestyle modification and periodic monitoring are recommended.",

        "Newly Diagnosed Diabetes":
        "Laboratory findings meet the diagnostic criteria for Type 2 Diabetes Mellitus. Further clinical evaluation and treatment planning are recommended.",

        "Controlled Diabetes":
        "Glycemic parameters demonstrate improvement and indicate satisfactory diabetes management. Continued monitoring and adherence to therapy are advised.",

        "Uncontrolled Diabetes":
        "Persistent hyperglycemia suggests inadequate glycemic control and an increased risk of diabetes-related complications.",

        "High-Risk Diabetes with Dyslipidemia":
        "Laboratory findings indicate uncontrolled Type 2 Diabetes Mellitus with associated dyslipidemia. Elevated LDL cholesterol, reduced HDL cholesterol, and increased triglyceride levels suggest an elevated cardiovascular risk."
    }

    return remarks.get(
        category,
        "Clinical correlation and further evaluation are recommended."
    )

# -----------------------------
# Generate PDFs
# -----------------------------
for _, row in df.iterrows():

    filename = (
        f"reports_pdf/"
        f"{row['Patient_ID']}_{row['Month']}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    elements = []

    title = Paragraph(
        "<b>ABC DIAGNOSTIC LABORATORY</b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1,12))

    patient_info = f"""
    <b>Patient ID:</b> {row['Patient_ID']}<br/>
    <b>Patient Name:</b> {row['Patient_Name']}<br/>
    <b>Age:</b> {row['Age']}<br/>
    <b>Gender:</b> {row['Gender']}<br/>
    <b>Month:</b> {row['Month']}
    """

    elements.append(
        Paragraph(patient_info, styles["Normal"])
    )

    elements.append(Spacer(1,12))

    data = [
        ["Test","Value","Unit"],
        ["HbA1c", row["HbA1c(%)"], "%"],
        ["FBS", row["FBS (mg/dL)"], "mg/dL"],
        ["PPBS", row["PPBS (mg/dL)"], "mg/dL"],
        ["LDL", row["LDL"], "mg/dL"],
        ["HDL", row["HDL"], "mg/dL"],
        ["Triglycerides", row["Triglycerides"], "mg/dL"]
    ]

    table = Table(data)

    table.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
        ])
    )

    elements.append(table)

    elements.append(Spacer(1,12))

    remark = get_remark(row["Category"])

    elements.append(
        Paragraph(
            f"<b>Doctor Remarks:</b><br/>{remark}",
            styles["Normal"]
        )
    )

    doc.build(elements)

print("All PDFs generated successfully.")