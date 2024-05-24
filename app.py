import streamlit as st
import language_tool_python
import nltk

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the LanguageTool object for English
tool = language_tool_python.LanguageTool('en-US')

# Function to check spelling and grammar
def check_spelling_and_grammar(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Initialize lists to store spelling and grammar issues
    spelling_issues = []
    grammar_issues = []
    
    # Initialize an empty list to store corrected sentences
    corrected_sentences = []
    
    # Iterate over each sentence
    for sentence in sentences:
        # Check spelling
        matches = tool.check(sentence)
        for match in matches:
            spelling_issue = {
                "sentence": sentence,
                "error": match.message,
                "suggestions": match.replacements,
                "context": match.context,
                "offset": match.offset,
                "length": match.errorLength
            }
            spelling_issues.append(spelling_issue)
        
        # Check grammar
        matches = tool.check(sentence)
        for match in matches:
            grammar_issue = {
                "sentence": sentence,
                "error": match.message,
                "suggestions": match.replacements,
                "context": match.context,
                "offset": match.offset,
                "length": match.errorLength
            }
            grammar_issues.append(grammar_issue)
        
        # Correct errors in the sentence
        corrected_sentence = language_tool_python.utils.correct(sentence, matches)
        corrected_sentences.append(corrected_sentence)
    
    # Join the corrected sentences into a single text
    corrected_text = ' '.join(corrected_sentences)
    
    return spelling_issues, grammar_issues, corrected_text

# Streamlit app
def main():
    st.title("WordWarden: Spelling and Grammar Checker")
    
    # Input text area
    text_input = st.text_area("Enter your text here:")
    
    # Check button
    if st.button("Check"):
        # Check spelling and grammar and get corrected text
        spelling_issues, grammar_issues, corrected_text = check_spelling_and_grammar(text_input)
        
        # Display corrected text
        st.subheader("Corrected Text:")
        st.write(corrected_text)
        
        # Display spelling issues
        if spelling_issues:
            st.subheader("Spelling Issues:")
            for issue in spelling_issues:
                st.write(f"Sentence: {issue['sentence']}")
                st.write(f"Error: {issue['error']}")
                st.write(f"Suggestions: {', '.join(issue['suggestions'])}")
                st.write(f"Context: {issue['context']}")
                st.write(f"Offset: {issue['offset']}")
                st.write(f"Length: {issue['length']}")
                st.write("\n")
        else:
            st.write("No spelling issues found.")
        
        # Display grammar issues
        if grammar_issues:
            st.subheader("Grammar Issues:")
            for issue in grammar_issues:
                st.write(f"Sentence: {issue['sentence']}")
                st.write(f"Error: {issue['error']}")
                st.write(f"Suggestions: {', '.join(issue['suggestions'])}")
                st.write(f"Context: {issue['context']}")
                st.write(f"Offset: {issue['offset']}")
                st.write(f"Length: {issue['length']}")
                st.write("\n")
        else:
            st.write("No grammar issues found.")

if __name__ == "__main__":
    main()