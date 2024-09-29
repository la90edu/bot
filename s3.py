import streamlit as st
import time
from questions import questions  # ייבוא השאלות מקובץ חיצוני

# הוספת סגנון CSS ליישור הטקסט מימין לשמאל עבור הבוט ולשמאל עבור המשתמש
def add_css():
    st.markdown(
        """
        <style>
        .css-1d391kg p, .css-1d391kg div, .css-1d391kg .stMarkdown {
            direction: rtl;
            text-align: right;
        }
        .stChatMessage {
            direction: rtl;
            text-align: right;
        }
        textarea {
            direction: rtl;
            text-align: right;
        }
        /* עיצוב הכפתורים */
        .stButton button {
            direction: rtl;
            text-align: right;
            float: right;
        }
        /* הצמדת הודעות המשתמש לשמאל */
        .stChatMessageUser {
            direction: ltr;  /* יישור הודעות המשתמש משמאל לימין */
            text-align: left;  /* הצמדת התגובה לשמאל */
        }
        </style>
        """, unsafe_allow_html=True
    )

# אפקט הקלדה
def typewriter_effect(text):
    response_container = st.empty()  # יצירת מיכל ריק לאפקט ההקלדה
    typed_response = ""
    for char in text:
        typed_response += char
        response_container.markdown(typed_response)
        time.sleep(0.02)  # ניתן לשנות את המהירות כאן

# פונקציה להצגת שאלה סגורה עם אפשרויות
def show_closed_question(question, options, feedbacks):
    if (st.session_state.question_state==0):
    # הצגת השאלה הסגורה מהבוט
        with st.chat_message("assistant"):
            #st.markdown(question)
            typewriter_effect(question)

    # יצירת כפתורים לבחירת תשובה
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            # הוספת השאלה והתשובה להיסטוריה
                st.session_state.question_state=1
                st.session_state.messages.append({"role": "assistant", "content": question})
                st.session_state.messages.append({"role": "user", "content": option})
                #st.rerun()
    
    if (st.session_state.question_state==1):
            # הוספת הפידבק עם אפקט הקלדה
            st.session_state.current_question += 1
            with st.chat_message("assistant"):
                typewriter_effect(feedbacks[i])  # אפקט הקלדה עבור הפידבק
            st.session_state.messages.append({"role": "assistant", "content": feedbacks[i]})
            st.rerun()

# פונקציה להצגת שאלה פתוחה
def show_open_question(question, feedback):
    # הצגת השאלה הפתוחה מהבוט עם אפקט הקלדה
    with st.chat_message("assistant"):
        typewriter_effect(question)

# פונקציה להצגת היסטוריית השיחה
def show_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# פונקציה להצגת תיבת הקלט הקבועה בתחתית
def display_input_box(disabled):
    user_input = st.chat_input("הכנס את התשובה שלך כאן", disabled=disabled)
    
    if user_input:
        # אם המשתמש מקליד לאחר סיום השאלות, נוסיף להיסטוריה בלבד
        if st.session_state.current_question >= len(questions):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "תודה! השיחה הסתיימה, אבל אני כאן לשמוע אם יש עוד משהו שתרצה לשתף."})
        # אם המשתמש מקליד תשובה לשאלה פתוחה
        elif not disabled:
            # הוספת התשובה להיסטוריה
            st.session_state.messages.append({"role": "user", "content": user_input})

            # טיפול בשאלה הפתוחה או החזרה לשאלה הסגורה
            if st.session_state.current_question < len(questions):
                current_q = questions[st.session_state.current_question]

                # אם זו שאלה פתוחה, נציג את הפידבק עם אפקט הקלדה
                if current_q["type"] == "open":
                    with st.chat_message("assistant"):
                        typewriter_effect(current_q["feedback"])  # אפקט ההקלדה לפידבק
                    st.session_state.messages.append({"role": "assistant", "content": current_q["feedback"]})
                    st.session_state.current_question += 1
                # אם זו שאלה סגורה, השאלה תוצג מחדש כדי שהמשתמש יבחר באחת האפשרויות
                elif current_q["type"] == "closed":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["question"]})
            
        st.rerun()

# הפונקציה הראשית
def main():
    st.title("שאלון בוט")
    
    # הוספת הסגנון לשיחה
    add_css()

    # אתחול משתני session_state במידת הצורך
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_question = 0
        st.session_state.finished = False
        st.session_state.question_state=0

        # הוספת משפט פתיחה
        opening_message = """
        שלום, אני ביטי הבוט של תוכנית ההייטק הלאומית. נעים מאוד!
        אני כאן כדי לשמוע על הרצון והמוטיבציה שלך להשתלב בעתיד בתפקידים שונים בתעשיית ההייטק.
        נתחיל מכמה שאלות בסיסיות.
        """
        st.session_state.messages.append({"role": "assistant", "content": opening_message})
        with st.chat_message("assistant"):
            typewriter_effect(opening_message)

    else: 
        # הצגת היסטוריית השיחה
        show_chat_history()

    # הצגת השאלה הנוכחית (אם עדיין לא סיימנו את כל השאלות)
    if not st.session_state.finished:
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            if current_q["type"] == "open":
                show_open_question(current_q["question"], current_q["feedback"])
                display_input_box(disabled=False)  # הפעלת תיבת ה-input
            elif current_q["type"] == "closed":
                show_closed_question(current_q["question"], current_q["options"], current_q["feedbacks"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
        else:
            st.session_state.finished = True
            summary_message = """
            שמחתי לשוחח איתכם ולשמוע על רמת המוטיבציה שלכם להשתלב בתחום טכנולוגי בעתיד. 
            אני ממליץ לכם בחום לדבר על הנושא עם מורה, הורה או איש צוות בבית הספר שיוכל לספר לכם עוד על התחום.
            """
            st.session_state.messages.append({"role": "assistant", "content": summary_message})
            #st.markdown(summary_message)
            with st.chat_message("assistant"):
                typewriter_effect(summary_message)
            
            display_input_box(disabled=False)  # השארת תיבת ה-input פעילה גם בסוף

if __name__ == "__main__":
    main()
