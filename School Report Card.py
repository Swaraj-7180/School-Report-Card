import hashlib
import datetime
import streamlit as st

# Define a Block
class ReportCardBlock:
    def __init__(self, student_name, marks, previous_hash=''):
        self.timestamp = str(datetime.datetime.now())
        self.student_name = student_name
        self.marks = marks  # Dictionary: subject -> marks
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = self.timestamp + self.student_name + str(self.marks) + self.previous_hash
        return hashlib.sha256(data.encode()).hexdigest()

# Blockchain to store report cards
class ReportCardBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return ReportCardBlock("Genesis", {}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_report_card(self, student_name, marks):
        previous_hash = self.get_latest_block().hash
        new_block = ReportCardBlock(student_name, marks, previous_hash)
        self.chain.append(new_block)

    def get_chain_data(self):
        chain_data = []
        for i, block in enumerate(self.chain):
            chain_data.append({
                "Block": i,
                "Student Name": block.student_name,
                "Marks": block.marks,
                "Timestamp": block.timestamp,
                "Previous Hash": block.previous_hash,
                "Hash": block.hash
            })
        return chain_data

# Initialize the blockchain
report_card_chain = ReportCardBlockchain()

# Streamlit interface
st.title('Report Card Blockchain')
st.write("Welcome to the Report Card Blockchain app. You can add student report cards, and view them on the blockchain.")

# Add report card form
with st.form(key="report_card_form"):
    student_name = st.text_input("Student Name")
    math_marks = st.number_input("Math Marks", min_value=0, max_value=100)
    science_marks = st.number_input("Science Marks", min_value=0, max_value=100)
    english_marks = st.number_input("English Marks", min_value=0, max_value=100)
    
    submit_button = st.form_submit_button("Add Report Card")

    if submit_button:
        if student_name:
            marks = {
                "Math": math_marks,
                "Science": science_marks,
                "English": english_marks
            }
            report_card_chain.add_report_card(student_name, marks)
            st.success(f"Report card for {student_name} added successfully!")
        else:
            st.error("Please provide a student name.")

# Display the blockchain
st.subheader("Blockchain Data")
chain_data = report_card_chain.get_chain_data()
st.write(chain_data)
