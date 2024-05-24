import streamlit as st
from transformers import pipeline
from happytransformer import HappyTextToText, TTSettings

# Initialize the spelling correction pipeline
fix_spelling = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")

# Initialize the grammar correction model
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

# Streamlit app
def main():
    st.title("Spelling and Grammar Checker")
    
    # Input text area
    text_input = st.text_area("Enter your text here:")
    
    # Check button
    if st.button("Check"):
        # Spelling correction
        corrected_spelling = fix_spelling(text_input)[0]['generated_text']
        
        # Grammar correction
        result = happy_tt.generate_text(f"grammar: {text_input}", args=args)
        corrected_grammar = result.text
        
        # Display corrected text
        st.subheader("Corrected Text:")
        st.write(corrected_grammar)  # Display grammar-corrected text
        
        # Display spelling correction if there's a difference
        if corrected_spelling != corrected_grammar:
            st.write(f"Spelling was also corrected to: {corrected_spelling}")

if __name__ == "__main__":
    main()
