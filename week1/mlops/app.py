import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import LabelEncoder
from transformers import pipeline

# Set up the Streamlit app layout
st.set_page_config(page_title="AutoML with LLM Chatbot", layout="wide")
st.title("AutoML Application with LLM Chatbot")

# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Upload Data", "Data Exploration", "Model Training", "AI Chatbot"])

# 1. Data Upload
if options == "Upload Data":
    st.header("Upload Your Dataset")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("Dataset Preview:")
        st.dataframe(df.head())
        st.session_state['df'] = df

# 2. Data Exploration
if options == "Data Exploration":
    st.header("Explore Your Data")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.write("Basic Statistics:")
        st.write(df.describe())
        
        st.subheader("Correlation Matrix")
        # Drop non-numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        if not numeric_df.empty:
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            st.pyplot(plt)
        else:
            st.write("No numeric data available for correlation matrix.")
        
        st.subheader("Data Distribution")
        columns = st.multiselect("Select columns to visualize", df.columns)
        if columns:
            df[columns].hist(bins=20, figsize=(10, 5))
            st.pyplot(plt)
    else:
        st.write("Please upload a dataset first!")

# 3. Model Training
if options == "Model Training":
    st.header("Train a Machine Learning Model")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        target_column = st.selectbox("Select Target Column", df.columns)
        features = df.drop(columns=[target_column]).columns.tolist()
        X = df[features]
        y = df[target_column]
        
        # Handle categorical features if any
        X = pd.get_dummies(X, drop_first=True)
        
        model_choice = st.selectbox("Choose a model", ["Logistic Regression", "Decision Tree", "Random Forest"])
        test_size = st.slider("Test Size (as a percentage)", min_value=0.1, max_value=0.5, value=0.3)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        if st.button("Train Model"):
            if model_choice == "Logistic Regression":
                model = LogisticRegression(max_iter=1000)
            elif model_choice == "Decision Tree":
                model = DecisionTreeClassifier()
            elif model_choice == "Random Forest":
                model = RandomForestClassifier()
                
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            st.write(f"Model Accuracy: {accuracy}")
            
            # Confusion Matrix
            st.subheader("Confusion Matrix")
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(cm, annot=True, fmt='d', cmap="coolwarm")
            st.pyplot(plt)
            
            # ROC Curve
            if len(np.unique(y_test)) == 2:  # Binary classification only
                st.subheader("ROC Curve")
                y_prob = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                roc_auc = auc(fpr, tpr)
                plt.figure()
                plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
                plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
                plt.xlim([0.0, 1.0])
                plt.ylim([0.0, 1.05])
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('Receiver Operating Characteristic')
                plt.legend(loc="lower right")
                st.pyplot(plt)
    else:
        st.write("Please upload and explore your dataset first!")

# 4. LLM-based Chatbot
if options == "AI Chatbot":
    st.header("AI Chatbot Assistant")
    
    chat_history = []
    if 'chat_history' in st.session_state:
        chat_history = st.session_state['chat_history']
    
    user_input = st.text_input("You: ", "")
    
    if user_input:
        # Use a small pre-trained model like GPT-2 small to run locally
        nlp = pipeline("text-generation", model="gpt2", max_length=50)
        response = nlp(user_input)[0]["generated_text"]
        chat_history.append((user_input, response))
        st.session_state['chat_history'] = chat_history
    
    if chat_history:
        st.subheader("Chat History")
        for question, answer in chat_history:
            st.write(f"You: {question}")
            st.write(f"Bot: {answer}")

# Footer
st.sidebar.info("This is a demo AutoML application with a simple chatbot.")
