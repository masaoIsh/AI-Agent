# ============================================================
# 🧩 Multi-Agent Consensus Protocol — Interactive Full Demo
# ============================================================

import math
from scipy import stats


# ------------------------------------------------------------
# Step 1 — Collect inputs
# ------------------------------------------------------------
def process_1_collect(agent_data):
    print("[Step 1] Collecting agent inputs")
    print("→ Each agent provides: direction (-1 SELL / 0 HOLD / +1 BUY), confidence (0–1), and reliability (0–1).")
    for k, v in agent_data.items():
        print(f"  {k:<12} d={v['direction']:+}, c={v['confidence']:.2f}, r={v['reliability']:.2f}")
    return agent_data


# ------------------------------------------------------------
# Step 2 — Unanimous Hold Shortcut (Rule 4)
# ------------------------------------------------------------
def process_2_unanimous_hold(agent_data):
    print("\n[Step 2] Rule 4 — Unanimous Hold Shortcut")
    all_hold = all(d["direction"] == 0 for d in agent_data.values())
    all_conf = all(d["confidence"] >= 0.6 for d in agent_data.values())
    all_rel = all(d["reliability"] > 0.5 for d in agent_data.values())

    print(f"  all_hold={all_hold}, all_conf≥0.6={all_conf}, all_rel>0.5={all_rel}")
    if all_hold and all_conf and all_rel:
        print("✅ All agents confidently HOLD → End debate immediately.")
        return True
    print("→ No unanimous confident HOLD detected. Continue evaluation.")
    return False


# ------------------------------------------------------------
# Step 3 — Minimum Confidence Threshold (Rule 1)
# ------------------------------------------------------------
def process_3_min_conf(agent_data):
    print("\n[Step 3] Rule 1 — Minimum Confidence Threshold")
    confidences = [d["confidence"] for d in agent_data.values()]
    min_conf = min(confidences)
    print(f"  min(confidences) = {min_conf:.3f}")
    if min_conf < 0.5:
        print("⚠️ Minimum confidence < 0.5 → Continue debate.")
        return False
    print("✅ Confidence threshold satisfied.")
    return True


# ------------------------------------------------------------
# Step 4 — Directional Conflict (Rule 2)
# ------------------------------------------------------------
def process_4_conflict(agent_data):
    print("\n[Step 4] Rule 2 — Directional Conflict Check")
    dirs = [d["direction"] for d in agent_data.values()]
    if 1 in dirs and -1 in dirs:
        print("⚠️ Found BUY(+1) and SELL(-1) positions.")
        for a1, d1 in agent_data.items():
            for a2, d2 in agent_data.items():
                if d1["direction"] == 1 and d2["direction"] == -1:
                    r1, r2 = d1["reliability"], d2["reliability"]
                    c1, c2 = d1["confidence"], d2["confidence"]
                    if r1 > 0.5 and r2 > 0.5 and (c1 > 0.5 or c2 > 0.5):
                        print(f"  {a1} vs {a2}: reliable (>{0.5}) & confident (>{0.5}) → Continue debate.")
                        return False
    print("✅ No critical directional conflict detected.")
    return True


# ------------------------------------------------------------
# Step 5 — Normalized Total Vibe (Rule 3)
# ------------------------------------------------------------
def process_5_vibe(agent_data):
    print("\n[Step 5] Rule 3 — Normalized Total Vibe Check")
    values = [d["direction"] * d["confidence"] for d in agent_data.values()]
    print(f"  Components (d×c): {values}")
    V = sum(values) / 3
    print(f"  V = ({'+'.join([f'{v:.2f}' for v in values])}) / 3 = {V:.3f}")
    if abs(V) < 0.5:
        print(f"⚠️ |V| = {abs(V):.2f} < 0.5 → Continue debate.")
        return False
    print(f"✅ |V| = {abs(V):.2f} ≥ 0.5 → Directional coherence reached.")
    return True


# ------------------------------------------------------------
# Step 6 — Compute Final Value & t-test
# ------------------------------------------------------------
def process_6_value(agent_data):
    print("\n[Step 6] Value Computation and Statistical Test")
    values = [d["direction"] * d["confidence"] * d["reliability"] for d in agent_data.values()]
    total_value = sum(values)
    print(f"  Contributions = {[f'{v:+.3f}' for v in values]}")
    print(f"  Total Value = {total_value:+.3f}")

    t_stat, p_val = stats.ttest_1samp(values, 0)
    print(f"  t-stat = {t_stat:.3f}, p-value = {p_val:.3f}")

    if abs(total_value) < 1e-5 or p_val >= 0.05:
        decision = "HOLD"
        print("⚪ Statistically inconclusive → HOLD.")
    elif total_value > 0:
        decision = "BUY"
        print("🟢 Significant positive value → BUY.")
    else:
        decision = "SELL"
        print("🔴 Significant negative value → SELL.")
    return decision, total_value, p_val


# ------------------------------------------------------------
# Step 7 — Summary
# ------------------------------------------------------------
def process_7_summary(agent_data, decision, value, p_val):
    print("\n[Step 7] Final Summary")
    print("=" * 60)
    for k, v in agent_data.items():
        print(f"  {k:<12}: d={v['direction']:+}, c={v['confidence']:.2f}, r={v['reliability']:.2f}")
    print("-" * 60)
    print(f"  Final Decision : {decision}")
    print(f"  Value          : {value:+.3f}")
    print(f"  p-value        : {p_val:.3f}")
    print("=" * 60)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    print("🧮 Multi-Agent Consensus Protocol — Full Interactive Demo")
    print("=" * 60)

    agents = ["fundamental", "sentiment", "valuation"]
    agent_data = {}

    for a in agents:
        print(f"\n⚙️ {a.title()} Agent Input")
        while True:
            try:
                d = int(input("  Direction (-1 SELL / 0 HOLD / +1 BUY): "))
                if d in [-1, 0, 1]:
                    break
            except ValueError:
                pass
            print("❌ Enter -1, 0, or +1.")
        while True:
            try:
                c = float(input("  Confidence (0–1): "))
                if 0 <= c <= 1:
                    break
            except ValueError:
                pass
            print("❌ Enter a number between 0 and 1.")
        while True:
            try:
                r = float(input("  Reliability (0–1): "))
                if 0 <= r <= 1:
                    break
            except ValueError:
                pass
            print("❌ Enter a number between 0 and 1.")
        agent_data[a] = {"direction": d, "confidence": c, "reliability": r}

    # Run all steps
    process_1_collect(agent_data)

    if process_2_unanimous_hold(agent_data):
        print("\n🏁 Final Decision: HOLD (Unanimous High-Confidence Neutrality)")
        return

    if not process_3_min_conf(agent_data):
        print("\n🔄 Debate continues (Low confidence).")
        return
    if not process_4_conflict(agent_data):
        print("\n🔄 Debate continues (Strong conflict).")
        return
    if not process_5_vibe(agent_data):
        print("\n🔄 Debate continues (Weak overall alignment).")
        return

    decision, total_value, p_val = process_6_value(agent_data)
    process_7_summary(agent_data, decision, total_value, p_val)


if __name__ == "__main__":
    main()
