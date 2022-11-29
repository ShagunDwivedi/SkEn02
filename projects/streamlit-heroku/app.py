import streamlit as st

st.write("""
# Subtraction of 2 Numbers App
This app gives the difference between two numbers.
""")
#Get Input

st.header('Input Numbers:')


def user_input_features():
    num1 = st.number_input("Insert Number-1")
    num2 = st.number_input("Insert Number-2")
    
    return(num1, num2)

num1, num2 = user_input_features()

st.subheader("Difference:")
st.write(num1-num2)