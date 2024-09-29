import streamlit as st
from questions import questions  # ייבוא השאלות מקובץ חיצוני

# הוספת CSS לעיצוב
def local_css(file_name):
    with open(file_name, encoding='utf-8') as f:  # הגדרת הקידוד ל-UTF-8
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# פונקציה להצגת שאלה סגורה עם אפשרויות
def show_closed_question(question, options, feedbacks):
    st.markdown(f"<div class='bot-message'><strong>{question}</strong></div>", unsafe_allow_html=True)
    
    # יצירת עמודות כך שכל כפתור יופיע בעמודה משלו
    cols = st.columns(len(options))  # מספר העמודות יהיה לפי מספר האפשרויות
    for i, option in enumerate(options):
        # כל כפתור יוצג בעמודה המתאימה לו
        if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            st.session_state.chat_history.append((question, option, feedbacks[i]))  # הוספת השאלה, התשובה והפידבק להיסטוריה
            st.session_state.current_question += 1
            st.rerun()

# פונקציה להצגת שאלה פתוחה עם st.chat_input
def show_open_question():
    question = "אנא ספר לנו מה אתה חושב על השאלון"
    st.markdown(f"<div class='bot-message'><strong>{question}</strong></div>", unsafe_allow_html=True)
    
    # הצגת תיבת קלט תחתונה בעזרת st.chat_input
    user_answer = st.chat_input("הכנס את התשובה שלך כאן")

    if user_answer:  # רק אם המשתמש כתב משהו
        st.session_state.chat_history.append((question, user_answer, "מעניייין מה שאתה אומר!"))  # פידבק קבוע
        st.session_state.finished = True
        st.rerun()

# פונקציה להצגת השיחה הקודמת והגלילה האוטומטית להתכתבות האחרונה
def show_chat_history():
    # הצגת ההיסטוריה של השאלות, התשובות והפידבקים
    for i, (question, answer, feedback) in enumerate(st.session_state.chat_history):
        st.markdown(f"<div class='bot-message'><strong>{question}</strong></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='user-message'>{answer}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-message'>{feedback}</div>", unsafe_allow_html=True)

    # # יצירת עוגן ריק בתחתית הדף אליו נוכל "לגלול"
    # scroll_placeholder = st.empty()
    # scroll_placeholder.markdown("<div id='scroll-to-here'></div>", unsafe_allow_html=True)

# הפונקציה הראשית
def main():
    st.title("בוט עם תשובות סגורות ופתוחות - עיצוב מותאם אישית")
    
    # שימוש ב-CSS מותאם אישית מתוך קובץ CSS חיצוני
    local_css("style.css")
    
    # בדיקה אם ההיסטוריה קיימת ב-session_state, אם לא, יוצרים אותה
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
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
        st.markdown("<div class='bot-message'>סיימת את כל השאלות! תודה שהשתתפת.</div>", unsafe_allow_html=True)

    # גלילה אוטומטית להתכתבות האחרונה
    st.markdown("<script>document.getElementById('scroll-to-here').scrollIntoView();</script>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
