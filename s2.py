import streamlit as st
from questions import questions  # ייבוא השאלות מקובץ חיצוני

# פונקציה להצגת שאלה סגורה עם אפשרויות
def show_closed_question(question, options, feedbacks):
    # הצגת השאלה בתיבת השיחה בפורמט של הודעת עוזר
    with st.chat_message("assistant"):
        st.markdown(question)
    
    # יצירת עמודות כך שכל כפתור יופיע בעמודה משלו
    cols = st.columns(len(options))  # מספר העמודות יהיה לפי מספר האפשרויות
    for i, option in enumerate(options):
        # כל כפתור יוצג בעמודה המתאימה לו
        if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            # שמירת השאלה והתשובה שנבחרה כ"הודעת עוזר" ו"הודעת משתמש" בהתאמה
            st.session_state.messages.append({"role": "assistant", "content": question})
            st.session_state.messages.append({"role": "user", "content": option})
            st.session_state.messages.append({"role": "assistant", "content": feedbacks[i]})
            st.session_state.current_question += 1
            st.rerun()

# פונקציה להצגת שאלה פתוחה עם st.chat_input
def show_open_question():
    question = "אנא ספר לנו מה אתה חושב על השאלון"
    
    # הצגת השאלה בתיבת השיחה בפורמט של הודעת עוזר
    with st.chat_message("assistant"):
        st.markdown(question)
    
    # הצגת תיבת קלט תחתונה בעזרת st.chat_input
    user_answer = st.chat_input("הכנס את התשובה שלך כאן")

    if user_answer:  # רק אם המשתמש כתב משהו
        st.session_state.messages.append({"role": "user", "content": user_answer})
        st.session_state.messages.append({"role": "assistant", "content": "מעניין מה שאתה אומר!"})  # פידבק קבוע
        st.session_state.finished = True
        st.rerun()

# פונקציה להצגת השיחה הקודמת
def show_chat_history():
    # הצגת ההיסטוריה של השאלות, התשובות והפידבקים
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# הפונקציה הראשית
def main():
    st.title("בוט עם תשובות סגורות ופתוחות")
    
    # בדיקה אם ההיסטוריה קיימת ב-session_state, אם לא, יוצרים אותה
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_question = 0
        st.session_state.finished = False

    # הצגת היסטוריית השיחה
    show_chat_history()

    # הצגת השאלה הנוכחית (אם עדיין לא סיימנו את השאלות)
    if not st.session_state.finished:
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            show_closed_question(current_q['question'], current_q['options'], current_q['feedbacks'])
        else:
            show_open_question()  # הצגת השאלה הפתוחה בסוף השאלון
    else:
        st.session_state.messages.append({"role": "assistant", "content": "סיימת את כל השאלות! תודה שהשתתפת."})
        with st.chat_message("assistant"):
            st.markdown("סיימת את כל השאלות! תודה שהשתתפת.")

if __name__ == "__main__":
    main()
