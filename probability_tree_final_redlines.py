
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Interactive Probability Tree")

# Sidebar inputs
st.sidebar.header("Inputs")

# Manually entered top-level probabilities
p_wrong = st.sidebar.number_input("Probability: Completed Wrong", min_value=0.0, max_value=1.0, value=0.15)
p_skipped = st.sidebar.number_input("Probability: Skipped", min_value=0.0, max_value=1.0, value=0.2)
p_right = st.sidebar.number_input("Probability: Completed Correctly", min_value=0.0, max_value=1.0, value=0.65)

# Check if probabilities are valid
total_p = p_wrong + p_skipped + p_right
is_valid = abs(total_p - 1.0) < 0.01
label_color = "black" if is_valid else "red"

# Subtree inputs
p_fix = st.sidebar.slider("P(Gets Fixed | Completed Wrong)", 0.0, 1.0, 0.5)

v_fix = st.sidebar.number_input("Value: Gets Fixed", value=-2.0)
v_stays_wrong = st.sidebar.number_input("Value: Never Fixed (Stays wrong)", value=3.0)
v_skipped = st.sidebar.number_input("Value: Skipped", value=-0.5)
v_right_val = st.sidebar.number_input("Value: Completed Correctly", value=8.0)

# Normalize for math safety
if total_p > 0:
    norm_wrong = p_wrong / total_p
    norm_skipped = p_skipped / total_p
    norm_right = p_right / total_p
else:
    norm_wrong = norm_skipped = norm_right = 1/3

# Expected value calculation
ev_wrong = norm_wrong * (p_fix * v_fix + (1 - p_fix) * v_stays_wrong)
ev_skip = norm_skipped * v_skipped
ev_correct = norm_right * v_right_val
ev_total = ev_wrong + ev_skip + ev_correct

st.subheader(f"Expected Value: {ev_total:.2f}")
if not is_valid:
    st.warning(f"⚠️ The top-level probabilities must sum to 1. Currently: {total_p:.2f}")

# Draw tree
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("off")

def draw_box(text, x, y):
    ax.text(x, y, text, ha='center', va='center',
            bbox=dict(boxstyle="round", facecolor="white"), fontsize=10)

def draw_arrow(x1, y1, x2, y2, label="", color="black", offset=0.05):
    ax.annotate("", xy=(x2, y2+0.01), xytext=(x1, y1-0.01),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="gray"))
    label_x = (x1 + x2) / 2
    label_y = (y1 + y2) / 2 + offset
    ax.text(label_x, label_y, label, ha="center", fontsize=9, color=color)

# Coordinates
y0, y1, y2 = 1.0, 0.8, 0.6
x_wrong, x_skip, x_right = 0.2, 0.5, 0.8
x_fix, x_stays_wrong = 0.1, 0.3
y3 = 0.4

# Arrows from root
draw_arrow(0.5, y0, x_wrong, y1, f"{norm_wrong:.2f}", color=label_color)
draw_arrow(0.5, y0, x_skip, y1, f"{norm_skipped:.2f}", color=label_color)
draw_arrow(0.5, y0, x_right, y1, f"{norm_right:.2f}", color=label_color)

# First level boxes
draw_box("Completed Wrong", x_wrong, y1)
draw_box(f"Skipped\n→ {v_skipped:.2f}", x_skip, y1)
draw_box(f"Completed Correctly\n→ {v_right_val:.2f}", x_right, y1)

# Arrows under Wrong
draw_arrow(x_wrong, y1, x_fix, y3, f"{p_fix:.2f}")
draw_arrow(x_wrong, y1, x_stays_wrong, y3, f"{(1 - p_fix):.2f}")

# Outcome boxes under Wrong
draw_box(f"Gets Fixed\n→ {v_fix:.2f}", x_fix, y3)
draw_box(f"Never Fixed\n(stays wrong)\n→ {v_stays_wrong:.2f}", x_stays_wrong, y3)

st.pyplot(fig)
