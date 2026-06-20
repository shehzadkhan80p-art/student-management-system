import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
[data-testid="stSidebar"]{
    background-color:#f5f7fa;
}

h1{
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FILE CONFIG
# =====================================================

FILE_NAME = "students.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "ID",
        "Name",
        "Age",
        "Class",
        "Email",
        "Marks",
        "Grade"
    ])
    df.to_csv(FILE_NAME, index=False)

# =====================================================
# FUNCTIONS
# =====================================================

def load_data():
    return pd.read_csv(FILE_NAME)

def save_data(data):
    data.to_csv(FILE_NAME, index=False)

def calculate_grade(marks):

    if marks >= 80:
        return "A"

    elif marks >= 70:
        return "B"

    elif marks >= 60:
        return "C"

    elif marks >= 50:
        return "D"

    else:
        return "Fail"

def create_pdf(student):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10,
             txt="Student Record",
             ln=True,
             align="C")

    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Student ID : {student['ID']}", ln=True)
    pdf.cell(200, 10, txt=f"Name : {student['Name']}", ln=True)
    pdf.cell(200, 10, txt=f"Age : {student['Age']}", ln=True)
    pdf.cell(200, 10, txt=f"Class : {student['Class']}", ln=True)
    pdf.cell(200, 10, txt=f"Email : {student['Email']}", ln=True)
    pdf.cell(200, 10, txt=f"Marks : {student['Marks']}", ln=True)
    pdf.cell(200, 10, txt=f"Grade : {student['Grade']}", ln=True)

    file_name = f"Student_{student['ID']}.pdf"

    pdf.output(file_name)

    return file_name

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# TITLE
# =====================================================

st.title("🎓 Student Record Management System")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📚 Navigation")

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Dashboard",
        "Add Student",
        "View Students",
        "Search Student",
        "Update Student",
        "Delete Student",
        "Student Marks",
        "Download PDF"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    total_students = len(df)

    average_marks = 0

    if len(df) > 0:
        average_marks = round(df["Marks"].mean(), 2)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Average Marks", average_marks)

# =====================================================
# ADD STUDENT
# =====================================================

elif menu == "Add Student":

    st.header("➕ Add Student")

    student_id = st.text_input("Student ID")

    name = st.text_input("Student Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=18
    )

    student_class = st.text_input("Class")

    email = st.text_input("Email")

    marks = st.number_input(
        "Marks",
        min_value=0,
        max_value=100,
        value=0
    )

    if st.button("Save Student"):

        if student_id.strip() == "":
            st.error("Student ID Required")

        elif student_id in df["ID"].astype(str).values:
            st.error("Student ID Already Exists")

        else:

            grade = calculate_grade(marks)

            new_student = pd.DataFrame([{
                "ID": student_id,
                "Name": name,
                "Age": age,
                "Class": student_class,
                "Email": email,
                "Marks": marks,
                "Grade": grade
            }])

            df = pd.concat(
                [df, new_student],
                ignore_index=True
            )

            save_data(df)

            st.success("Student Added Successfully")

# =====================================================
# VIEW STUDENTS
# =====================================================

elif menu == "View Students":

    st.header("📋 Student Records")

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇ Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

# =====================================================
# SEARCH STUDENT
# =====================================================

elif menu == "Search Student":

    st.header("🔍 Search Student")

    search_id = st.text_input("Enter Student ID")

    if st.button("Search"):

        result = df[df["ID"].astype(str) == search_id]

        if result.empty:
            st.error("Student Not Found")

        else:
            st.dataframe(result)

# =====================================================
# UPDATE STUDENT
# =====================================================

elif menu == "Update Student":

    st.header("✏️ Update Student")

    search_id = st.text_input("Enter Student ID")

    result = df[df["ID"].astype(str) == search_id]

    if not result.empty:

        index = result.index[0]

        name = st.text_input(
            "Name",
            result.iloc[0]["Name"]
        )

        age = st.number_input(
            "Age",
            value=int(result.iloc[0]["Age"])
        )

        student_class = st.text_input(
            "Class",
            result.iloc[0]["Class"]
        )

        email = st.text_input(
            "Email",
            result.iloc[0]["Email"]
        )

        marks = st.number_input(
            "Marks",
            min_value=0,
            max_value=100,
            value=int(result.iloc[0]["Marks"])
        )

        if st.button("Update Record"):

            grade = calculate_grade(marks)

            df.loc[index, "Name"] = name
            df.loc[index, "Age"] = age
            df.loc[index, "Class"] = student_class
            df.loc[index, "Email"] = email
            df.loc[index, "Marks"] = marks
            df.loc[index, "Grade"] = grade

            save_data(df)

            st.success("Record Updated Successfully")

# =====================================================
# DELETE STUDENT
# =====================================================

elif menu == "Delete Student":

    st.header("❌ Delete Student")

    student_id = st.text_input("Enter Student ID")

    if st.button("Delete Student"):

        if student_id not in df["ID"].astype(str).values:

            st.error("Student Not Found")

        else:

            df = df[df["ID"].astype(str) != student_id]

            save_data(df)

            st.success("Student Deleted Successfully")

# =====================================================
# STUDENT MARKS
# =====================================================

elif menu == "Student Marks":

    st.header("📚 Student Marks Report")

    if len(df) == 0:

        st.warning("No Student Records Available")

    else:

        marks_df = df[
            ["ID", "Name", "Marks", "Grade"]
        ]

        st.dataframe(
            marks_df,
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Marks",
                round(df["Marks"].mean(), 2)
            )

        with col2:
            st.metric(
                "Highest Marks",
                int(df["Marks"].max())
            )

        with col3:
            st.metric(
                "Lowest Marks",
                int(df["Marks"].min())
            )

# =====================================================
# DOWNLOAD PDF
# =====================================================

elif menu == "Download PDF":

    st.header("📄 Download Student PDF")

    student_id = st.text_input("Enter Student ID")

    if st.button("Generate PDF"):

        result = df[
            df["ID"].astype(str) == student_id
        ]

        if result.empty:

            st.error("Student Not Found")

        else:

            student = result.iloc[0]

            pdf_file = create_pdf(student)

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="⬇ Download PDF",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf"
                )

            st.success("PDF Ready For Download")