import math
import streamlit as st

st.set_page_config(
    page_title="E-CELL | Virtual Electrochemistry Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f7fbff 0%, #eef7f5 48%, #fffaf2 100%);
    }
    .hero {
        padding: 2rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(120deg, #0f4c5c, #087f8c 55%, #35a7a0);
        color: white;
        box-shadow: 0 12px 35px rgba(15,76,92,.20);
        margin-bottom: 1.4rem;
    }
    .hero h1 { margin: 0; font-size: 2.8rem; }
    .hero p { margin: .5rem 0 0; font-size: 1.08rem; }
    .card {
        background: rgba(255,255,255,.90);
        padding: 1.2rem 1.3rem;
        border-radius: 18px;
        border: 1px solid rgba(15,76,92,.10);
        box-shadow: 0 8px 25px rgba(20,60,70,.08);
        margin-bottom: 1rem;
    }
    .metric {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #dbe9ea;
        text-align: center;
    }
    .metric .value { font-size: 1.7rem; font-weight: 700; color: #0f4c5c; }
    .metric .label { color: #567176; font-size: .9rem; }
    .flow {
        display:flex; align-items:center; justify-content:center; gap:18px;
        padding:1.3rem; background:white; border-radius:18px;
        border:1px solid #dbe9ea; margin:1rem 0;
        font-size:1.05rem;
    }
    .electrode { padding: .9rem 1.2rem; border-radius:14px; font-weight:700; }
    .anode { background:#fff0ed; color:#a33d2e; }
    .cathode { background:#eaf7ff; color:#17658a; }
    .arrow { font-size:1.7rem; color:#0f4c5c; }
    .small { color:#5e7277; font-size:.9rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
HALF_CELLS = {
    "Zn²⁺/Zn": {"E": -0.76, "ion": "Zn²⁺", "metal": "Zn", "n": 2},
    "Fe²⁺/Fe": {"E": -0.44, "ion": "Fe²⁺", "metal": "Fe", "n": 2},
    "Ni²⁺/Ni": {"E": -0.25, "ion": "Ni²⁺", "metal": "Ni", "n": 2},
    "Cu²⁺/Cu": {"E": 0.34, "ion": "Cu²⁺", "metal": "Cu", "n": 2},
    "Ag⁺/Ag": {"E": 0.80, "ion": "Ag⁺", "metal": "Ag", "n": 1},
}

F = 96485.0
R = 8.314462618

# ---------- Helpers ----------
def card(title, body):
    st.markdown(f'<div class="card"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)

def emf(cathode, anode):
    return cathode["E"] - anode["E"]

def n_for_pair(a, b):
    # Common educational half-cells above are 1e or 2e.
    # LCM gives balanced electron count.
    return math.lcm(a["n"], b["n"])

# ---------- Header ----------
st.markdown("""
<div class="hero">
<h1>⚡ E-CELL</h1>
<p>Virtual Electrochemistry Lab · Galvanic Cells · Nernst Equation · Gibbs Free Energy</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("## 🧪 E-CELL")
st.sidebar.caption("Interactive Engineering Chemistry learning lab")
page = st.sidebar.radio(
    "LAB MODULES",
    ["🏠 Home", "🔋 Galvanic Cell", "🧮 Nernst Calculator", "⚡ Gibbs Free Energy", "📚 Theory & Quiz"],
)
st.sidebar.divider()
st.sidebar.markdown("**Project**")
st.sidebar.caption("E-CELL – Virtual Electrochemistry Lab")
st.sidebar.caption("Python + Streamlit")

# ---------- Home ----------
if page == "🏠 Home":
    st.markdown("### Welcome to your virtual lab")
    st.write("Explore electrochemical cells through interactive selection, calculations, theory notes and a self-check quiz.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric"><div class="value">🔋</div><div class="label">Galvanic Cell Simulator</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric"><div class="value">🧮</div><div class="label">Nernst Equation</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric"><div class="value">⚡</div><div class="label">Gibbs Free Energy</div></div>', unsafe_allow_html=True)

    st.markdown("### What you can do")
    cols = st.columns(2)
    with cols[0]:
        card("🔋 Galvanic Cell", "Select two half-cells and identify the anode, cathode, electron direction and standard cell potential.")
        card("🧮 Nernst Calculator", "Calculate cell potential under non-standard conditions using Ecell = E°cell − (RT/nF) ln Q.")
    with cols[1]:
        card("⚡ Gibbs Free Energy", "Connect cell potential with spontaneity using ΔG = −nFEcell.")
        card("📚 Theory + Quiz", "Revise the core concepts and test your understanding with a short self-assessment.")

    st.info("Tip: Start with the Galvanic Cell module and try Zn²⁺/Zn with Cu²⁺/Cu to reproduce the Daniell-cell example from the project report.")

# ---------- Galvanic Cell ----------
elif page == "🔋 Galvanic Cell":
    st.markdown("## 🔋 Galvanic Cell Simulator")
    st.write("Choose two half-cells. E-CELL compares their standard reduction potentials and assigns the cathode and anode.")

    left, right = st.columns(2)
    with left:
        h1 = st.selectbox("Half-cell 1", list(HALF_CELLS.keys()), index=0)
    with right:
        h2 = st.selectbox("Half-cell 2", list(HALF_CELLS.keys()), index=3)

    if h1 == h2:
        st.warning("Choose two different half-cells.")
    else:
        a = HALF_CELLS[h1]
        b = HALF_CELLS[h2]

        # Higher reduction potential is cathode in spontaneous galvanic direction.
        if a["E"] > b["E"]:
            cath_name, cath = h1, a
            an_name, an = h2, b
        else:
            cath_name, cath = h2, b
            an_name, an = h1, a

        E0 = emf(cath, an)
        n = n_for_pair(cath, an)

        st.markdown("### Cell analysis")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric"><div class="value">{E0:.2f} V</div><div class="label">E°cell</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric"><div class="value">{an_name}</div><div class="label">Anode · oxidation</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric"><div class="value">{cath_name}</div><div class="label">Cathode · reduction</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="flow">
            <div class="electrode anode">ANODE<br><small>{an_name}</small></div>
            <div class="arrow">e⁻ →</div>
            <div class="electrode cathode">CATHODE<br><small>{cath_name}</small></div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"Spontaneous galvanic direction: {an_name} → {cath_name}. E°cell = {E0:.2f} V.")
        st.markdown("### Cell notation")
        st.code(f"{an['metal']} | {an['ion']} || {cath['ion']} | {cath['metal']}", language="text")

        st.markdown("### Half-reaction roles")
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"**Oxidation at anode**  \n{an['metal']} → {an['ion']} + e⁻")
        with r2:
            st.markdown(f"**Reduction at cathode**  \n{cath['ion']} + e⁻ → {cath['metal']}")

        st.caption("E°cell = E°cathode − E°anode. Positive E°cell indicates spontaneity in the represented direction.")

# ---------- Nernst ----------
elif page == "🧮 Nernst Calculator":
    st.markdown("## 🧮 Nernst Equation Calculator")
    st.write("Calculate the cell potential at a selected temperature and reaction quotient.")

    c1, c2 = st.columns(2)
    with c1:
        E0 = st.number_input("E°cell (V)", value=1.10, step=0.01, format="%.4f")
        n = st.number_input("Number of electrons, n", min_value=1, value=2, step=1)
    with c2:
        T = st.number_input("Temperature (K)", min_value=1.0, value=298.0, step=1.0)
        Q = st.number_input("Reaction quotient, Q", min_value=0.000001, value=1.0, step=0.1, format="%.6f")

    if st.button("Calculate Ecell", type="primary"):
        E = E0 - (R * T / (n * F)) * math.log(Q)
        st.markdown("### Result")
        st.markdown(f'<div class="metric"><div class="value">{E:.4f} V</div><div class="label">Cell potential, Ecell</div></div>', unsafe_allow_html=True)

        if abs(Q - 1.0) < 1e-12:
            st.info("Because Q = 1, ln(Q) = 0, so Ecell = E°cell.")
        st.code(f"Ecell = E°cell − (RT/nF) ln Q\n     = {E0:.4f} − (8.314 × {T:.1f} / ({n} × 96485)) × ln({Q})\n     = {E:.4f} V", language="text")

    st.markdown("### At 298 K")
    st.latex(r"E_{\mathrm{cell}} = E^\circ_{\mathrm{cell}}-\frac{0.0591}{n}\log Q")
    st.caption("Use temperature in kelvin. Q must be a positive number.")

# ---------- Gibbs ----------
elif page == "⚡ Gibbs Free Energy":
    st.markdown("## ⚡ Gibbs Free Energy Calculator")
    st.write("Use ΔG = −nFEcell to connect electrochemical potential with reaction spontaneity.")

    c1, c2 = st.columns(2)
    with c1:
        n = st.number_input("Number of electrons, n", min_value=1, value=2, step=1, key="g_n")
    with c2:
        E = st.number_input("Cell potential, Ecell (V)", value=1.10, step=0.01, format="%.4f", key="g_e")

    if st.button("Calculate ΔG", type="primary"):
        dg_j = -n * F * E
        dg_kj = dg_j / 1000
        st.markdown("### Result")
        st.markdown(f'<div class="metric"><div class="value">{dg_kj:.3f} kJ mol⁻¹</div><div class="label">Gibbs free-energy change, ΔG</div></div>', unsafe_allow_html=True)

        if dg_j < 0:
            st.success("ΔG is negative: the represented reaction direction is spontaneous under the selected conditions.")
        elif dg_j > 0:
            st.warning("ΔG is positive: the represented reaction direction is non-spontaneous.")
        else:
            st.info("ΔG = 0: the system is at equilibrium.")

        st.code(f"ΔG = −nFE\n   = −({n}) × 96485 × ({E:.4f})\n   = {dg_j:.2f} J mol⁻¹\n   = {dg_kj:.3f} kJ mol⁻¹", language="text")

# ---------- Theory + Quiz ----------
else:
    st.markdown("## 📚 Theory & Quiz")

    tabs = st.tabs(["📖 Theory", "📝 Quiz"])

    with tabs[0]:
        sections = {
            "Oxidation & Reduction":
                "Oxidation is loss of electrons and reduction is gain of electrons. Oxidation occurs at the anode; reduction occurs at the cathode.",
            "Galvanic Cell":
                "A galvanic cell converts chemical energy from a spontaneous redox reaction into electrical energy. A Daniell cell is a common example using zinc and copper half-cells connected by an external wire and salt bridge.",
            "Cell Potential":
                "E°cell = E°cathode − E°anode. A positive E°cell indicates spontaneity under standard conditions for the represented reaction direction.",
            "Nernst Equation":
                "Ecell = E°cell − (RT/nF) ln Q. At 298 K, Ecell = E°cell − (0.0591/n) log Q.",
            "Gibbs Free Energy":
                "ΔG = −nFEcell. Negative ΔG indicates a spontaneous reaction in the represented direction; zero indicates equilibrium; positive ΔG indicates a non-spontaneous direction.",
        }
        for title, body in sections.items():
            card(title, body)

    with tabs[1]:
        questions = [
            ("1. In a galvanic cell, oxidation occurs at the:", ["Cathode", "Anode", "Salt bridge", "External wire"], 1),
            ("2. For a spontaneous galvanic reaction, E°cell is generally:", ["Negative", "Zero", "Positive", "Always 0.0591"], 2),
            ("3. Which equation relates cell potential to Gibbs free energy?", ["ΔG = nFE", "ΔG = −nFE", "E = nF/ΔG", "Q = nFE"], 1),
            ("4. In the Daniell cell Zn²⁺/Zn and Cu²⁺/Cu, the cathode is:", ["Zn", "Cu", "Both", "Salt bridge"], 1),
            ("5. When Q = 1, the Nernst correction term is:", ["Maximum", "Zero", "Negative infinity", "Undefined"], 1),
        ]

        score = 0
        for i, (q, options, answer) in enumerate(questions):
            choice = st.radio(q, options, key=f"quiz_{i}")
            if options.index(choice) == answer:
                score += 1

        if st.button("Show Quiz Score", type="primary"):
            st.success(f"Your score: {score}/{len(questions)}")
            if score == len(questions):
                st.balloons()
            elif score >= 3:
                st.info("Good work! Review the theory once more and try again.")
            else:
                st.warning("Review the theory section and retry the quiz.")

# ---------- Footer ----------
st.divider()
st.caption("E-CELL · Virtual Electrochemistry Lab · Educational simulation")
