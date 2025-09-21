# frontend/dashboard.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib
import json

# ====== Configure your backend URL here ======
API_BASE_URL = "https://resume-evalution-system-backend.onrender.com"  # change if needed

# ================= Helper / API utilities =================
def _try_endpoints(endpoint_variants):
    """Try endpoints in order; return (response_obj, used_url) or (None, None)."""
    for ep in endpoint_variants:
        url = API_BASE_URL.rstrip("/") + ep  # ep already contains leading slash
        try:
            resp = requests.get(url, timeout=6)
        except Exception:
            resp = None
        if resp is None:
            continue
        if resp.status_code in (200, 201):
            try:
                return resp.json(), url
            except Exception:
                return resp.text, url
        # allow 204 for delete etc.
    return None, None

def call_api(method, endpoint, data=None, files=None, timeout=20):
    """
    Attempt API call. Tries endpoint and endpoint with/without trailing slash.
    Returns (success_flag, parsed_json_or_status).
    """
    variants = [endpoint]
    if endpoint.endswith("/"):
        variants.append(endpoint.rstrip("/"))
    else:
        variants.append(endpoint + "/")

    for ep in variants:
        url = API_BASE_URL.rstrip("/") + ep
        try:
            if method.upper() == "GET":
                r = requests.get(url, timeout=timeout)
            elif method.upper() == "POST":
                if files is not None:
                    # when sending files, `data` can be used for form fields
                    r = requests.post(url, files=files, data=data, timeout=timeout)
                else:
                    r = requests.post(url, json=data, timeout=timeout)
            elif method.upper() == "DELETE":
                r = requests.delete(url, timeout=timeout)
            else:
                return False, f"Unsupported method {method}"
        except Exception as e:
            # network error -> try next variant
            continue

        if r.status_code in (200, 201):
            # try parse json
            try:
                return True, r.json()
            except Exception:
                return True, r.text
        elif r.status_code == 204:
            return True, None
        else:
            # try next variant
            continue

    return False, None

def normalize_list_response(resp, key_names):
    """
    Given a response `resp`, try to normalize to a Python list.
    key_names: a list of candidate keys to search for (e.g. ["resumes","data"])
    """
    if resp is None:
        return None
    if isinstance(resp, list):
        return resp
    if isinstance(resp, dict):
        # try provided keys
        for k in key_names:
            if k in resp and isinstance(resp[k], list):
                return resp[k]
        # try to find first list value
        for v in resp.values():
            if isinstance(v, list):
                return v
        # it's a single object -> return as single-item list
        return [resp]
    # if it's a string or other -> no list
    return None

# ================= Session-state initialization (local fallback) ==============
if "local_resumes" not in st.session_state:
    st.session_state.local_resumes = []  # list of dicts: id, filename, student_name, student_email, created_at
if "local_jobs" not in st.session_state:
    st.session_state.local_jobs = []     # list of dicts: id, title, company, location, content, created_at
if "local_evals" not in st.session_state:
    st.session_state.local_evals = []    # list of evaluation dicts

def next_local_id(collection):
    return (max([item.get("id", 0) for item in collection]) + 1) if collection else 1

# =================== Data getters that prefer backend but fall back ===============
def get_resumes():
    ok, resp = call_api("GET", "/resumes")
    if ok:
        lst = normalize_list_response(resp, ["resumes"])
        if lst is not None:
            return lst, True
    # fallback: try GET /resumes/ specifically
    ok2, resp2 = call_api("GET", "/resumes/")
    if ok2:
        lst = normalize_list_response(resp2, ["resumes"])
        if lst is not None:
            return lst, True
    # fallback to local
    return st.session_state.local_resumes, False

def get_job_descriptions():
    ok, resp = call_api("GET", "/job-descriptions")
    if ok:
        lst = normalize_list_response(resp, ["job_descriptions", "job_descriptions_list", "jobs"])
        if lst is not None:
            return lst, True
    ok2, resp2 = call_api("GET", "/job-descriptions/")
    if ok2:
        lst = normalize_list_response(resp2, ["job_descriptions", "job_descriptions_list", "jobs"])
        if lst is not None:
            return lst, True
    return st.session_state.local_jobs, False

def get_evaluations():
    ok, resp = call_api("GET", "/evaluations")
    if ok:
        lst = normalize_list_response(resp, ["evaluations"])
        if lst is not None:
            return lst, True
    ok2, resp2 = call_api("GET", "/evaluations/")
    if ok2:
        lst = normalize_list_response(resp2, ["evaluations"])
        if lst is not None:
            return lst, True
    return st.session_state.local_evals, False

# =================== Upload helpers ===================
def upload_resume_to_backend(file_bytes, filename, student_name="", student_email=""):
    files = {"file": (filename, file_bytes)}
    data = {"student_name": student_name, "student_email": student_email}
    ok, resp = call_api("POST", "/resumes/", data=data, files=files)
    return ok, resp

def upload_job_to_backend(file_bytes, filename, title="", company="", location=""):
    files = {"file": (filename, file_bytes)}
    data = {"title": title, "company": company, "location": location}
    ok, resp = call_api("POST", "/job-descriptions/", data=data, files=files)
    return ok, resp

def post_evaluation_to_backend(payload):
    ok, resp = call_api("POST", "/evaluations/", data=payload)
    return ok, resp

# =================== Mock evaluation generator (fallback) ===================
def deterministic_score(seed_str):
    # deterministic pseudo-random using hash
    h = int(hashlib.sha256(seed_str.encode("utf-8")).hexdigest()[:8], 16)
    return 50 + (h % 51)  # 50..100

def generate_mock_evaluation(resume, job):
    # resume and job are dicts; use filename/title to seed
    seed = f"{resume.get('filename','')}-{job.get('title', job.get('filename',''))}"
    overall = deterministic_score(seed)
    hard = max(30, overall - 10)
    semantic = min(100, overall + 5)
    matched = ["communication", "teamwork"] if overall > 60 else []
    missing = ["aws", "docker"] if overall < 80 else []
    eval_entry = {
        "id": next_local_id(st.session_state.local_evals),
        "resume_filename": resume.get("filename"),
        "job_title": job.get("title", job.get("filename")),
        "relevance_score": float(overall),
        "hard_match_score": float(hard),
        "semantic_match_score": float(semantic),
        "verdict": "High" if overall >= 80 else ("Medium" if overall >= 60 else "Low"),
        "matched_skills": matched,
        "missing_skills": missing,
        "strengths": ["Clear formatting", "Relevant internships"] if overall > 60 else [],
        "weaknesses": ["Missing cloud experience"] if overall < 80 else [],
        "improvement_suggestions": "Quantify achievements, add projects." if overall < 85 else "Great resume!",
        "overall_feedback": "Good match." if overall >= 60 else "Needs improvement.",
        "created_at": datetime.now().isoformat()
    }
    return eval_entry

# =================== UI: Pages implementations ===================
def page_dashboard():
    st.header("📊 Dashboard")
    resumes, r_ok = get_resumes()
    jobs, j_ok = get_job_descriptions()
    evals, e_ok = get_evaluations()

    num_resumes = len(resumes) if resumes else 0
    num_jobs = len(jobs) if jobs else 0
    num_evals = len(evals) if evals else 0
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resumes", num_resumes)
    col2.metric("Job Descriptions", num_jobs)
    col3.metric("Evaluations", num_evals)
    if num_evals > 0:
        avg_score = sum(e.get("relevance_score", 0) for e in evals) / num_evals
        col4.metric("Avg Score", f"{avg_score:.1f}")
    else:
        col4.metric("Avg Score", "N/A")

    st.markdown("---")
    st.subheader("Quick Actions")
    c1, c2, c3 = st.columns(3)
    if c1.button("Upload Resume"):
        st.session_state.page = "Upload Resume"
    if c2.button("Upload Job Description"):
        st.session_state.page = "Upload Job Description"
    if c3.button("Evaluate Resume"):
        st.session_state.page = "Evaluate Resume"

    st.markdown("---")
    st.subheader("Recent Evaluations")
    if evals:
        recent = sorted(evals, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
        for ev in recent:
            st.write(f"• ID {ev.get('id')} — {ev.get('resume_filename')} vs {ev.get('job_title')} — {ev.get('relevance_score'):.1f} — {ev.get('verdict')}")
    else:
        st.info("No evaluations yet (backend may be down or no data uploaded).")

def page_upload_resume():
    st.header("📄 Upload Resume")
    with st.form("upload_resume_form"):
        student_name = st.text_input("Student name", "")
        student_email = st.text_input("Student email", "")
        uploaded = st.file_uploader("Select resume file (pdf/docx/txt)", type=["pdf", "docx", "txt"])
        submit = st.form_submit_button("Upload")
    if submit:
        if not uploaded:
            st.error("Please choose a file.")
            return
        file_bytes = uploaded.getvalue()
        filename = uploaded.name
        ok, resp = upload_resume_to_backend(file_bytes, filename, student_name, student_email)
        if ok:
            st.success("Uploaded to backend successfully.")
            # update local caches if backend returned created resource
            created = None
            if isinstance(resp, dict):
                # try to extract resource (some backends return {"id":..., ...})
                # add to local view if it seems like a resume object
                if "filename" in resp or "student_name" in resp:
                    created = resp
            # if no resource returned, still append a local representation for UI
            if created is None:
                created = {
                    "id": next_local_id(st.session_state.local_resumes),
                    "filename": filename,
                    "student_name": student_name or "Unknown",
                    "student_email": student_email or "Unknown",
                    "created_at": datetime.now().isoformat()
                }
            st.session_state.local_resumes.append(created)
        else:
            st.warning("Backend upload failed — saving locally for UI use.")
            created = {
                "id": next_local_id(st.session_state.local_resumes),
                "filename": filename,
                "student_name": student_name or "Unknown",
                "student_email": student_email or "Unknown",
                "created_at": datetime.now().isoformat()
            }
            st.session_state.local_resumes.append(created)
            st.success("Saved locally (temporary).")

def page_upload_job():
    st.header("💼 Upload Job Description")
    with st.form("upload_job_form"):
        title = st.text_input("Job title", "")
        company = st.text_input("Company", "")
        location = st.text_input("Location", "")
        uploaded = st.file_uploader("Select job description file (pdf/docx/txt)", type=["pdf", "docx", "txt"])
        submit = st.form_submit_button("Upload")
    if submit:
        if not uploaded and not title:
            st.error("Please provide a file or a title.")
            return
        filename = uploaded.name if uploaded else f"{title}.txt"
        file_bytes = uploaded.getvalue() if uploaded else b""
        ok, resp = upload_job_to_backend(file_bytes, filename, title, company, location)
        if ok:
            st.success("Uploaded to backend successfully.")
            created = None
            if isinstance(resp, dict):
                if "title" in resp or "filename" in resp:
                    created = resp
            if created is None:
                created = {
                    "id": next_local_id(st.session_state.local_jobs),
                    "title": title or filename,
                    "company": company or "Unknown",
                    "location": location or "Unknown",
                    "content": "",
                    "created_at": datetime.now().isoformat()
                }
            st.session_state.local_jobs.append(created)
        else:
            st.warning("Backend upload failed — saving locally for UI use.")
            created = {
                "id": next_local_id(st.session_state.local_jobs),
                "title": title or filename,
                "company": company or "Unknown",
                "location": location or "Unknown",
                "content": "",
                "created_at": datetime.now().isoformat()
            }
            st.session_state.local_jobs.append(created)
            st.success("Saved locally (temporary).")

def page_evaluate():
    st.header("🔍 Evaluate Resume")
    resumes, r_ok = get_resumes()
    jobs, j_ok = get_job_descriptions()

    if not resumes:
        st.info("No resumes available. Upload one first.")
        return
    if not jobs:
        st.info("No job descriptions available. Upload one first.")
        return

    # Build selection lists
    resume_options = [(r.get("id") if "id" in r else r.get("filename"), r.get("filename")) for r in resumes]
    job_options = [(j.get("id") if "id" in j else j.get("title", j.get("filename")), j.get("title", j.get("filename"))) for j in jobs]

    resume_map = {str(k): r for k, r in zip([x[0] for x in resume_options], resumes)}
    job_map = {str(k): j for k, j in zip([x[0] for x in job_options], jobs)}

    resume_choice = st.selectbox("Choose resume", options=[str(x[0]) for x in resume_options],
                                format_func=lambda k: resume_map.get(k, {}).get("filename", k))
    job_choice = st.selectbox("Choose job description", options=[str(x[0]) for x in job_options],
                              format_func=lambda k: job_map.get(k, {}).get("title", k))

    if st.button("Run Evaluation"):
        resume_obj = resume_map[resume_choice]
        job_obj = job_map[job_choice]

        # Try backend evaluation: we post a payload to evaluations endpoint
        payload = {
            "resume": resume_obj,
            "job_description": job_obj
        }
        ok, resp = post_evaluation_to_backend(payload)
        if ok and isinstance(resp, dict):
            st.success("Evaluation received from backend.")
            # if backend returned an evaluation dict, show and store it
            eval_obj = resp
            # ensure created_at and id exist
            if "id" not in eval_obj:
                eval_obj["id"] = next_local_id(st.session_state.local_evals)
            if "created_at" not in eval_obj:
                eval_obj["created_at"] = datetime.now().isoformat()
            st.session_state.local_evals.append(eval_obj)
            display_single_evaluation(eval_obj)
        else:
            st.warning("Backend evaluation not available — generating local mock evaluation.")
            mock = generate_mock_evaluation(resume_obj, job_obj)
            st.session_state.local_evals.append(mock)
            display_single_evaluation(mock)

def display_single_evaluation(ev):
    st.markdown(f"### Evaluation: {ev.get('resume_filename','resume')} → {ev.get('job_title','job')}")
    st.metric("Relevance score", f"{ev.get('relevance_score',0):.1f}")
    st.write("**Verdict:**", ev.get("verdict", "N/A"))
    # show matched/missing
    st.write("**Matched skills:**", ", ".join(ev.get("matched_skills", [])) or "None")
    st.write("**Missing skills:**", ", ".join(ev.get("missing_skills", [])) or "None")
    # show charts if scores exist
    if "hard_match_score" in ev and "semantic_match_score" in ev:
        df = pd.DataFrame({
            "type": ["Hard", "Semantic", "Overall"],
            "score": [ev.get("hard_match_score",0), ev.get("semantic_match_score",0), ev.get("relevance_score",0)]
        })
        fig = px.bar(df, x="type", y="score", title="Score breakdown")
        st.plotly_chart(fig, use_container_width=True)
    st.write("**Feedback:**")
    st.write(ev.get("overall_feedback", ev.get("improvement_suggestions", "")))

def page_view_evaluations():
    st.header("📋 View Evaluations")
    evals, ok = get_evaluations()
    if not evals:
        st.info("No evaluations available.")
        return
    df = pd.DataFrame(evals)
    st.dataframe(df, use_container_width=True)

    # allow selecting an evaluation to see details
    eval_ids = [str(e.get("id")) for e in evals]
    choice = st.selectbox("Select evaluation to inspect", options=eval_ids, format_func=lambda x: f"ID {x}")
    sel = next((e for e in evals if str(e.get("id")) == choice), None)
    if sel:
        display_single_evaluation(sel)

def page_batch_processing():
    st.header("📦 Batch Processing")
    st.info("Upload multiple resumes and/or job descriptions, then run batch evaluations.")
    uploaded_resumes = st.file_uploader("Upload multiple resumes", type=["pdf","docx","txt"], accept_multiple_files=True)
    uploaded_jobs = st.file_uploader("Upload multiple job descriptions", type=["pdf","docx","txt"], accept_multiple_files=True)
    if st.button("Upload all and run mock evaluations"):
        # upload resumes
        uploaded_res_names = []
        for f in uploaded_resumes:
            filename = f.name
            ok, resp = upload_resume_to_backend(f.getvalue(), filename)
            if ok:
                uploaded_res_names.append(filename)
            else:
                # local fallback create
                created = {
                    "id": next_local_id(st.session_state.local_resumes),
                    "filename": filename,
                    "student_name": "Unknown",
                    "student_email": "unknown",
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.local_resumes.append(created)
                uploaded_res_names.append(filename)
        # upload jobs
        uploaded_job_titles = []
        for f in uploaded_jobs:
            filename = f.name
            ok, resp = upload_job_to_backend(f.getvalue(), filename)
            if ok:
                uploaded_job_titles.append(filename)
            else:
                created = {
                    "id": next_local_id(st.session_state.local_jobs),
                    "title": filename,
                    "company": "Unknown",
                    "location": "Unknown",
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.local_jobs.append(created)
                uploaded_job_titles.append(filename)
        st.success("Files uploaded (backend or local fallback). Now generating mock evaluations...")
        # create mock evaluations pairing each resume with each job (simple)
        resumes = st.session_state.local_resumes if st.session_state.local_resumes else []
        jobs = st.session_state.local_jobs if st.session_state.local_jobs else []
        for r in resumes:
            for j in jobs:
                mock = generate_mock_evaluation(r, j)
                st.session_state.local_evals.append(mock)
        st.success("Batch mock evaluations created in local session state.")

def page_manage_data():
    st.header("🗂 Manage Data")
    st.subheader("Resumes")
    resumes, r_ok = get_resumes()
    for r in resumes:
        cols = st.columns([4,1])
        cols[0].write(f"{r.get('id','-')} — {r.get('filename')} — {r.get('student_name','')}")
        if cols[1].button(f"Delete resume {r.get('id')}", key=f"del_resume_{r.get('id')}"):
            # attempt backend delete
            # try /resumes/{id} then /resumes/ with payload
            deleted = False
            if "id" in r:
                ok, _ = call_api("DELETE", f"/resumes/{r['id']}")
                if ok:
                    st.success("Deleted on backend (if endpoint exists). Refreshing view.")
                    deleted = True
            # remove from local store if present
            st.session_state.local_resumes = [x for x in st.session_state.local_resumes if x.get("id") != r.get("id")]
            if not deleted:
                st.info("Removed locally (backend may not have delete endpoint).")

    st.markdown("---")
    st.subheader("Job Descriptions")
    jobs, j_ok = get_job_descriptions()
    for j in jobs:
        cols = st.columns([4,1])
        cols[0].write(f"{j.get('id','-')} — {j.get('title')} — {j.get('company','')}")
        if cols[1].button(f"Delete job {j.get('id')}", key=f"del_job_{j.get('id')}"):
            if "id" in j:
                ok, _ = call_api("DELETE", f"/job-descriptions/{j['id']}")
                if ok:
                    st.success("Deleted on backend (if endpoint exists).")
            st.session_state.local_jobs = [x for x in st.session_state.local_jobs if x.get("id") != j.get("id")]
            st.info("Removed locally (if backend delete not supported).")

    st.markdown("---")
    st.subheader("Evaluations")
    evals, e_ok = get_evaluations()
    for ev in evals:
        cols = st.columns([4,1])
        cols[0].write(f"ID {ev.get('id')} — {ev.get('resume_filename')} vs {ev.get('job_title')} — {ev.get('relevance_score')}")
        if cols[1].button(f"Delete eval {ev.get('id')}", key=f"del_eval_{ev.get('id')}"):
            if "id" in ev:
                ok, _ = call_api("DELETE", f"/evaluations/{ev['id']}")
                if ok:
                    st.success("Deleted on backend (if endpoint exists).")
            st.session_state.local_evals = [x for x in st.session_state.local_evals if x.get("id") != ev.get("id")]
            st.info("Removed locally (if backend delete not supported).")

# ================= Main app wiring =================
def main():
    st.set_page_config(page_title="Resume Evaluation System", layout="wide")
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    with st.sidebar:
        st.title("Resume Eval")
        pages = ["Dashboard", "Upload Resume", "Upload Job Description", "Evaluate Resume", "View Evaluations", "Batch Processing", "Manage Data"]
        for p in pages:
            if st.button(p):
                st.session_state.page = p
                st.experimental_rerun()

        st.markdown("---")
        st.write("API status:")
        ok, _ = call_api("GET", "/")
        if ok:
            st.success("Backend reachable")
        else:
            st.error("Backend not reachable — using local fallback UI")

    st.markdown("<h1>📄 Resume Evaluation System</h1>", unsafe_allow_html=True)

    # route to page
    page = st.session_state.page
    if page == "Dashboard":
        page_dashboard()
    elif page == "Upload Resume":
        page_upload_resume()
    elif page == "Upload Job Description":
        page_upload_job()
    elif page == "Evaluate Resume":
        page_evaluate()
    elif page == "View Evaluations":
        page_view_evaluations()
    elif page == "Batch Processing":
        page_batch_processing()
    elif page == "Manage Data":
        page_manage_data()
    else:
        st.info("Select a page from the sidebar.")

if __name__ == "__main__":
    main()
