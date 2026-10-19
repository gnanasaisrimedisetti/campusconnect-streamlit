
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CampusConnect",
    page_icon="🎓",
    layout="wide"
)

# Store demo data during the current app session
if "students" not in st.session_state:
    st.session_state.students = []

if "clubs" not in st.session_state:
    st.session_state.clubs = []

if "memberships" not in st.session_state:
    st.session_state.memberships = []

if "events" not in st.session_state:
    st.session_state.events = []

# Website design
st.markdown("""
<style>
.stApp {
    background-color: #f5f8fc;
}
.main-title {
    background: linear-gradient(100deg, #12376a, #168aad);
    padding: 25px;
    border-radius: 15px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">'
    '<h1>🎓 CampusConnect</h1>'
    '<p>Smart College Club Membership and Event Management System</p>'
    '</div>',
    unsafe_allow_html=True
)

st.write("Welcome! Manage students, clubs, memberships and events.")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Students",
        "Clubs",
        "Memberships",
        "Events",
        "Set Operations"
    ]
)

students = st.session_state.students
clubs = st.session_state.clubs
memberships = st.session_state.memberships
events = st.session_state.events

def next_id(items):
    return max([item["id"] for item in items] + [0]) + 1

def show_table(items):
    if items:
        st.dataframe(
            pd.DataFrame(items),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No records available yet.")

if page == "Dashboard":
    st.header("📊 Dashboard")

    a, b, c, d = st.columns(4)
    a.metric("Students", len(students))
    b.metric("Clubs", len(clubs))
    c.metric("Memberships", len(memberships))
    d.metric("Events", len(events))

    st.subheader("Welcome to CampusConnect")
    st.write("Use the sidebar to manage college club activities.")

elif page == "Students":
    st.header("👨‍🎓 Student Management")

    with st.form("student_form"):
        name = st.text_input("Student Name")
        roll = st.text_input("Roll / ERP Number")
        department = st.text_input("Department", value="BTech")
        submitted = st.form_submit_button("Add Student")

    if submitted:
        if name.strip() and roll.strip():
            if any(s["roll"].lower() == roll.strip().lower()
                   for s in students):
                st.error("This roll number already exists.")
            else:
                students.append({
                    "id": next_id(students),
                    "name": name.strip(),
                    "roll": roll.strip(),
                    "department": department.strip()
                })
                st.success("Student added successfully!")
                st.rerun()
        else:
            st.error("Enter the student name and roll number.")

    st.subheader("Student List")
    show_table(students)

    if students:
        student_options = {
            f'{s["name"]} ({s["roll"]})': s["id"]
            for s in students
        }
        selected = st.selectbox(
            "Select student to delete",
            list(student_options)
        )

        if st.button("Delete Student"):
            student_id = student_options[selected]
            st.session_state.students = [
                s for s in students if s["id"] != student_id
            ]
            st.session_state.memberships = [
                m for m in memberships
                if m["student_id"] != student_id
            ]
            st.rerun()

elif page == "Clubs":
    st.header("🏫 Club Management")

    with st.form("club_form"):
        name = st.text_input("Club Name")
        category = st.selectbox(
            "Category",
            ["Technical", "Cultural", "Sports", "Arts", "Other"]
        )
        description = st.text_area("Club Description")
        submitted = st.form_submit_button("Add Club")

    if submitted:
        if name.strip():
            if any(c["name"].lower() == name.strip().lower()
                   for c in clubs):
                st.error("This club already exists.")
            else:
                clubs.append({
                    "id": next_id(clubs),
                    "name": name.strip(),
                    "category": category,
                    "description": description.strip()
                })
                st.success("Club added successfully!")
                st.rerun()
        else:
            st.error("Enter a club name.")

    st.subheader("Club List")
    show_table(clubs)

    if clubs:
        club_options = {
            f'{c["name"]} (ID {c["id"]})': c["id"]
            for c in clubs
        }
        selected = st.selectbox(
            "Select club to delete",
            list(club_options)
        )

        if st.button("Delete Club"):
            club_id = club_options[selected]
            st.session_state.clubs = [
                c for c in clubs if c["id"] != club_id
            ]
            st.session_state.memberships = [
                m for m in memberships
                if m["club_id"] != club_id
            ]
            st.session_state.events = [
                e for e in events if e["club_id"] != club_id
            ]
            st.rerun()

elif page == "Memberships":
    st.header("🤝 Club Memberships")

    if not students or not clubs:
        st.warning("Add at least one student and one club first.")
    else:
        student_options = {
            f'{s["name"]} ({s["roll"]})': s["id"]
            for s in students
        }
        club_options = {
            c["name"]: c["id"] for c in clubs
        }

        with st.form("membership_form"):
            student = st.selectbox(
                "Select Student", list(student_options)
            )
            club = st.selectbox(
                "Select Club", list(club_options)
            )
            submitted = st.form_submit_button("Register Membership")

        if submitted:
            sid = student_options[student]
            cid = club_options[club]

            exists = any(
                m["student_id"] == sid and m["club_id"] == cid
                for m in memberships
            )

            if exists:
                st.error("This student is already in this club.")
            else:
                memberships.append({
                    "id": next_id(memberships),
                    "student_id": sid,
                    "club_id": cid
                })
                st.success("Membership registered!")
                st.rerun()

    st.subheader("Membership List")
    student_names = {s["id"]: s["name"] for s in students}
    club_names = {c["id"]: c["name"] for c in clubs}

    rows = [
        {
            "ID": m["id"],
            "Student": student_names.get(m["student_id"], "Unknown"),
            "Club": club_names.get(m["club_id"], "Unknown")
        }
        for m in memberships
    ]
    show_table(rows)

elif page == "Events":
    st.header("🎉 Event Management")

    if not clubs:
        st.warning("Add a club before creating an event.")
    else:
        club_options = {c["name"]: c["id"] for c in clubs}

        with st.form("event_form"):
            title = st.text_input("Event Name")
            club = st.selectbox(
                "Organising Club", list(club_options)
            )
            event_date = st.date_input("Event Date")
            venue = st.text_input("Venue")
            description = st.text_area("Event Description")
            submitted = st.form_submit_button("Create Event")

        if submitted:
            if title.strip():
                events.append({
                    "id": next_id(events),
                    "title": title.strip(),
                    "club_id": club_options[club],
                    "date": str(event_date),
                    "venue": venue.strip(),
                    "description": description.strip()
                })
                st.success("Event created successfully!")
                st.rerun()
            else:
                st.error("Enter an event name.")

    st.subheader("Event List")
    club_names = {c["id"]: c["name"] for c in clubs}
    rows = [
        {
            "ID": e["id"],
            "Event": e["title"],
            "Club": club_names.get(e["club_id"], "Unknown"),
            "Date": e["date"],
            "Venue": e["venue"]
        }
        for e in events
    ]
    show_table(rows)

elif page == "Set Operations":
    st.header("🔢 Set Operations")

    if len(clubs) < 2:
        st.info("Add at least two clubs to compare their memberships.")
    else:
        club_options = {c["name"]: c["id"] for c in clubs}
        col1, col2 = st.columns(2)

        with col1:
            club_a = st.selectbox("Club A", list(club_options))
        with col2:
            club_b = st.selectbox(
                "Club B", list(club_options), index=1
            )

        A = {
            m["student_id"] for m in memberships
            if m["club_id"] == club_options[club_a]
        }
        B = {
            m["student_id"] for m in memberships
            if m["club_id"] == club_options[club_b]
        }

        student_names = {s["id"]: s["name"] for s in students}

        results = {
            "Union (A ∪ B)": A | B,
            "Intersection (A ∩ B)": A & B,
            "A − B": A - B,
            "B − A": B - A
        }

        for title, result in results.items():
            st.subheader(title)
            names = sorted(
                student_names.get(sid, f"Student {sid}")
                for sid in result
            )
            st.write(", ".join(names) if names else "No students")
            st.caption(f"Total students: {len(result)}")

st.divider()
st.caption(
    "CampusConnect | College Project Demo | "
    "This starter version stores data only during the current session."
)