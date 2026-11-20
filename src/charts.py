"""Charts for the article from the result tables: static PNGs at double resolution, readable at
phone width, one message per chart with the takeaway in the title.

    python src/charts.py                                   # results/*.csv -> results/charts/
    python src/charts.py --results results/dryrun --out results/dryrun/charts
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import PercentFormatter  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

import desk_aa  # noqa: E402
from paths import RESULTS  # noqa: E402

MODEL_ORDER = ("gemini", "jev", "clef")
MODEL_NAMES = {"gemini": "Gemini Decision 1", "jev": "Jev 1.14", "clef": "Clef"}
# Reference palette, categorical slots 1 to 3, validated all-pairs on the light surface.
MODEL_COLOURS = {"gemini": "#2a78d6", "jev": "#eb6834", "clef": "#1baf7a"}
SURFACE, INK, INK2, MUTED, GRID, BASELINE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
GROUP_NAMES = {
    "hijack_plain": "Plain hijack",
    "hijack_reviewer_naive": "Reviewer-aimed, naive",
    "hijack_reviewer_informed": "Reviewer-aimed, informed",
    "hijack_units": "Units trick",
    "hijack_extra_field": "Extra field",
    "hijack_swapped_target": "Swapped target",
    "hijack_scope_creep": "Scope creep",
    "hijack_policy_note": "Policy note",
    "hijack_false_premise": "False premise",
}
DPI = 200
FIG_W = 8.0
TABLE_FILES = ("accuracy", "operating_points", "fooling", "rewording", "speed", "cost")

plt.rcParams.update({
    "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"],
    "font.size": 14, "axes.titlesize": 14, "axes.labelsize": 13, "xtick.labelsize": 12, "ytick.labelsize": 13,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": BASELINE, "axes.linewidth": 1, "xtick.color": INK2, "ytick.color": INK,
    "text.color": INK, "axes.labelcolor": INK2, "legend.frameon": False, "legend.fontsize": 12,
})


def pct(x: float) -> str:
    if x == 0:
        return "0%"
    return f"{100 * x:.1f}%" if x < 0.095 else f"{100 * x:.0f}%"


def _names(models) -> str:
    names = [MODEL_NAMES[m] for m in models]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def _models_in(df: pd.DataFrame) -> list[str]:
    present = set(df.model_key)
    return [m for m in MODEL_ORDER if m in present]


def _style(ax) -> None:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def _dot_interval(ax, y, value, lo, hi, colour, label=None, filled=True) -> None:
    ax.plot([lo, hi], [y, y], color=colour, linewidth=2, solid_capstyle="round", zorder=2)
    ax.plot([value], [y], marker="o", markersize=11, color=colour if filled else SURFACE,
            markeredgecolor=colour if not filled else SURFACE, markeredgewidth=2, zorder=3)
    if label:
        ax.annotate(label, (hi, y), xytext=(7, 0), textcoords="offset points", va="center", fontsize=12, color=INK2)


def _finish(fig, path: Path, title: str, caption: str, top: float = 0.80, bottom: float = 0.16, left: float = 0.30) -> Path:
    wrapped = textwrap.fill(title, 64)
    lines = wrapped.count("\n") + 1
    fig.subplots_adjust(left=left, right=0.97, top=top - 0.05 * (lines - 1), bottom=bottom, wspace=0.35)
    fig.text(0.01, 0.985, wrapped, ha="left", va="top", fontsize=16, weight="semibold", color=INK, linespacing=1.25)
    fig.text(0.01, 0.015, textwrap.fill(caption, 110), ha="left", va="bottom", fontsize=10.5, color=MUTED)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path


def _y_models(ax, models) -> None:
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([MODEL_NAMES[m] for m in models])
    ax.set_ylim(len(models) - 0.5, -0.5)


def _xlim_pct(ax, hi_values, floor=0.05) -> None:
    top = max(max(hi_values) * 1.45, floor)
    ax.set_xlim(0, min(1.0, top))
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))


def titles(tables: dict) -> dict[str, str]:
    out = {}
    acc = tables["accuracy"].set_index("model_key")
    n = int(acc.n.iloc[0])
    if acc.misses.max() - acc.misses.min() <= 2 and acc.false_blocks.max() - acc.false_blocks.min() <= 2:
        out["errors_at_half"] = (f"At the default threshold the three models are level: {int(acc.misses.min())} to "
                                 f"{int(acc.misses.max())} hijacks let through and {int(acc.false_blocks.min())} to "
                                 f"{int(acc.false_blocks.max())} legitimate calls blocked, out of {n:,} rows")
    else:
        best = acc.miss_rate.idxmin()
        out["errors_at_half"] = (f"At the default threshold {MODEL_NAMES[best]} lets through the fewest hijacks: "
                                 f"{pct(acc.loc[best, 'miss_rate'])}, blocking {pct(acc.loc[best, 'false_block_rate'])} of legitimate calls")
    ops = tables["operating_points"]
    at5 = ops[ops.max_false_block_rate == 0.05].set_index("model_key")
    if at5.misses.max() == 0:
        out["operating_points"] = (f"With false blocks held to 5%, none of the three lets a single hijack through on the "
                                   f"{int(at5.n_hijack_report.iloc[0])} report-half hijacks")
    else:
        best5, worst5 = at5.miss_rate.idxmin(), at5.miss_rate.idxmax()
        out["operating_points"] = (f"Holding false blocks to 5%, {MODEL_NAMES[best5]} still lets {pct(at5.loc[best5, 'miss_rate'])} "
                                   f"of hijacks through and {MODEL_NAMES[worst5]} {pct(at5.loc[worst5, 'miss_rate'])}")
    fool = tables["fooling"]
    informed_b = fool[(fool.group == "hijack_reviewer_informed") & (fool.view == "B")].set_index("model_key")
    informed_a = fool[(fool.group == "hijack_reviewer_informed") & (fool.view == "A")].set_index("model_key")
    if len(informed_a) and (informed_a.miss_rate > informed_b.miss_rate).any():
        worst = informed_a.miss_rate.idxmax()
        out["fooling"] = (f"Seeing the planted text helps: with it hidden {MODEL_NAMES[worst]} lets "
                          f"{pct(informed_a.loc[worst, 'miss_rate'])} of informed attacks through, with it visible "
                          f"{pct(informed_b.loc[worst, 'miss_rate'])}")
    else:
        plain = fool[(fool.group == "hijack_plain") & (fool.view == "B")].set_index("model_key")
        worst = informed_b.miss_rate.idxmax()
        out["fooling"] = (f"Text written for the reviewer works: {MODEL_NAMES[worst]} lets {pct(informed_b.loc[worst, 'miss_rate'])} "
                          f"of informed attacks through against {pct(plain.loc[worst, 'miss_rate'])} of plain hijacks")
    rw = tables["rewording"]
    any_pair = rw[rw.pair == "any_pair"].set_index("model_key")
    if any_pair.flip_share.max() < 0.01:
        out["rewording"] = (f"Rewording the question changes under 1% of decisions for all three: "
                            f"{int(any_pair.flips.min())} to {int(any_pair.flips.max())} rows of {int(any_pair.n.iloc[0]):,}")
    else:
        most = any_pair.flip_share.idxmax()
        out["rewording"] = (f"Reword the question and {MODEL_NAMES[most]} changes {pct(any_pair.loc[most, 'flip_share'])} of its "
                            f"decisions; {MODEL_NAMES[any_pair.flip_share.idxmin()]} changes {pct(any_pair.flip_share.min())}")
    speed = tables["speed"]
    pooled = speed[speed.run == "pooled"].set_index("model_key")
    cost = tables["cost"].set_index("model_key")
    fastest, cheapest = pooled.median_ms.idxmin(), cost.usd_per_1000_decisions.idxmin()
    ms, usd = pooled.loc[fastest, "median_ms"], cost.loc[cheapest, "usd_per_1000_decisions"]
    if fastest == cheapest:
        out["speed_cost"] = (f"{MODEL_NAMES[fastest]} is both the fastest, {ms:.0f} ms a decision, and the cheapest, "
                             f"${usd:.3f} per 1,000 decisions")
    else:
        out["speed_cost"] = (f"{MODEL_NAMES[fastest]} answers in {ms:.0f} ms and {MODEL_NAMES[cheapest]} costs "
                             f"${usd:.3f} per 1,000 decisions")
    scores = desk_aa.SCORES
    without = {k: desk_aa.index(v, drop=desk_aa.KNOWLEDGE_AND_REASONING) for k, v in scores.items()}
    gap = without["Jev 1.14"] - without["Gemini Decision 1"]
    band = desk_aa.reweighted_gap_half_width(40)
    out["aa_reweighting"] = (f"Drop AA's knowledge and reasoning exams and its Jev vs Gemini tie becomes a {gap:.1f}-point Jev lead, "
                             f"at the edge of a ±{band:.1f}-point noise band")
    return out


def chart_errors_at_half(tables, out_dir, title) -> Path:
    acc = tables["accuracy"].set_index("model_key")
    models = _models_in(tables["accuracy"])
    fig, axes = plt.subplots(1, 2, figsize=(FIG_W, 3.9), sharey=True)
    panels = [("miss_rate", "miss_lo", "miss_hi", "Hijacks let through"),
              ("false_block_rate", "false_block_lo", "false_block_hi", "Legitimate calls blocked")]
    for ax, (col, lo, hi, name) in zip(axes, panels):
        for i, m in enumerate(models):
            _dot_interval(ax, i, acc.loc[m, col], acc.loc[m, lo], acc.loc[m, hi], MODEL_COLOURS[m], pct(acc.loc[m, col]))
        ax.set_title(name, loc="left", color=INK2, weight="normal")
        _y_models(ax, models)
        _xlim_pct(ax, acc[hi])
        _style(ax)
    n = int(acc.n.iloc[0])
    return _finish(fig, out_dir / "errors_at_half.png", title,
                   f"Decision at 0.5 on {n:,} rows. Dots are rates, lines are 95% Wilson intervals. Same route for all three.",
                   left=0.24)


def chart_operating_points(tables, out_dir, title) -> Path:
    ops = tables["operating_points"]
    models = _models_in(ops)
    fig, axes = plt.subplots(1, 2, figsize=(FIG_W, 3.9), sharey=True)
    for ax, budget in zip(axes, (0.01, 0.05)):
        sub = ops[ops.max_false_block_rate == budget].set_index("model_key")
        for i, m in enumerate(models):
            _dot_interval(ax, i, sub.loc[m, "miss_rate"], sub.loc[m, "miss_lo"], sub.loc[m, "miss_hi"], MODEL_COLOURS[m],
                          pct(sub.loc[m, "miss_rate"]))
        ax.set_title(f"False blocks capped at {100 * budget:.0f}%", loc="left", color=INK2, weight="normal", fontsize=13)
        _y_models(ax, models)
        _xlim_pct(ax, sub.miss_hi)
        _style(ax)
    n_h = int(ops.n_hijack_report.iloc[0])
    n_l = int(ops.n_legit_report.iloc[0])
    return _finish(fig, out_dir / "operating_points.png", title,
                   f"Hijacks let through at a threshold chosen on the tune half, measured on the report half: {n_h} hijacks, "
                   f"{n_l} legitimate calls. The 1% point rests on a handful of rows; 5% is the steadier figure.", left=0.24)


def chart_fooling(tables, out_dir, title) -> Path:
    fool = tables["fooling"]
    fool = fool[fool.group.isin(GROUP_NAMES)]
    models = _models_in(fool)
    groups = [g for g in GROUP_NAMES if g in set(fool.group)]
    fig, axes = plt.subplots(1, len(models), figsize=(FIG_W, 4.2), sharey=True, sharex=True)
    axes = list(axes) if len(models) > 1 else [axes]
    hi_values = []
    visible = fool[fool.view == "B"]
    xmax = min(1.0, max(float(visible.wrong_hi.max()) * 1.45, 0.05)) if len(visible) else 0.1
    for ax, m in zip(axes, models):
        sub = fool[fool.model_key == m]
        for i, g in enumerate(groups):
            b = sub[(sub.group == g) & (sub.view == "B")]
            a = sub[(sub.group == g) & (sub.view == "A")]
            if len(b):
                hi_values.append(float(b.wrong_hi.iloc[0]))
            if len(a) and len(b):
                ax.plot([a.miss_rate.iloc[0], b.miss_rate.iloc[0]], [i, i], color=MODEL_COLOURS[m], linewidth=2, zorder=1)
            if len(a):
                ax.plot([a.miss_rate.iloc[0]], [i], marker="o", markersize=10, color=SURFACE,
                        markeredgecolor=MODEL_COLOURS[m], markeredgewidth=2, zorder=2)
            if len(b):
                ax.plot([b.miss_rate.iloc[0]], [i], marker="o", markersize=11, color=MODEL_COLOURS[m],
                        markeredgecolor=SURFACE, markeredgewidth=2, zorder=3)
                value_b = float(b.miss_rate.iloc[0])
                value_a = float(a.miss_rate.iloc[0]) if len(a) else value_b
                low, high = min(value_a, value_b), max(value_a, value_b)
                ax.annotate(pct(high), (high, i), xytext=(10, 0), textcoords="offset points",
                            ha="left", va="center", fontsize=11, color=INK2)
                if high - low > 0.004:
                    if low > 0.25 * xmax:
                        ax.annotate(pct(low), (low, i), xytext=(-10, 0), textcoords="offset points",
                                    ha="right", va="center", fontsize=11, color=INK2)
                    else:
                        ax.annotate(pct(low), (low, i), xytext=(0, -11), textcoords="offset points",
                                    ha="center", va="top", fontsize=11, color=INK2)
        ax.set_title(MODEL_NAMES[m], loc="left", color=INK2, weight="normal")
        ax.set_yticks(range(len(groups)))
        ax.set_yticklabels([GROUP_NAMES[g] for g in groups])
        ax.set_ylim(len(groups) - 0.3, -0.7)
        _style(ax)
    axes[0].set_xlim(0, xmax)
    axes[0].xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    handles = [Line2D([], [], marker="o", color=SURFACE, markeredgecolor=INK2, markeredgewidth=2, markersize=9, linestyle="none"),
               Line2D([], [], marker="o", color=INK2, markersize=10, linestyle="none")]
    fig.legend(handles, ["Planted text hidden (View A)", "Planted text visible (View B)"], loc="lower right",
               bbox_to_anchor=(0.98, 0.075), ncol=2)
    return _finish(fig, out_dir / "fooling.png", title,
                   "Share of hijacks let through at 0.5, by who wrote them and whether the model saw the text they planted.",
                   left=0.28, bottom=0.28)


def chart_rewording(tables, out_dir, title) -> Path:
    rw = tables["rewording"]
    models = _models_in(rw)
    fig, axes = plt.subplots(1, 2, figsize=(FIG_W, 3.9), sharey=True)
    any_pair = rw[rw.pair == "any_pair"].set_index("model_key")
    for i, m in enumerate(models):
        _dot_interval(axes[0], i, any_pair.loc[m, "flip_share"], any_pair.loc[m, "flip_lo"], any_pair.loc[m, "flip_hi"],
                      MODEL_COLOURS[m], pct(any_pair.loc[m, "flip_share"]))
    axes[0].set_title("Decisions that change between wordings", loc="left", color=INK2, weight="normal", fontsize=13)
    _y_models(axes[0], models)
    _xlim_pct(axes[0], any_pair.flip_hi)
    _style(axes[0])
    pairs = rw[rw.pair != "any_pair"]
    worst = pairs.groupby("model_key").mean_abs_change.max()
    for i, m in enumerate(models):
        value = float(worst.get(m, 0.0))
        axes[1].plot([0, value], [i, i], color=MODEL_COLOURS[m], linewidth=10, solid_capstyle="round", zorder=2)
        axes[1].annotate(f"{value:.2f}", (value, i), xytext=(9, 0), textcoords="offset points", va="center", fontsize=12, color=INK2)
    axes[1].set_title("Largest mean probability swing", loc="left", color=INK2, weight="normal", fontsize=13)
    axes[1].set_xlim(0, max(float(worst.max()) * 1.6, 0.05))
    _style(axes[1])
    return _finish(fig, out_dir / "rewording.png", title,
                   "Three wordings of the same question: the main one, a paraphrase and a flipped version. Left: rows whose "
                   "allow or block decision differs between any two wordings. Right: the largest mean absolute change in the "
                   "probability across the three pairs.", left=0.24, bottom=0.27)


def chart_speed_cost(tables, out_dir, title) -> Path:
    speed = tables["speed"]
    pooled = speed[speed.run == "pooled"].set_index("model_key")
    cost = tables["cost"].set_index("model_key")
    models = [m for m in MODEL_ORDER if m in pooled.index and m in cost.index]
    fig, ax = plt.subplots(figsize=(FIG_W, 4.4))
    cheapest = cost.loc[models, "usd_per_1000_decisions"].idxmin()
    for m in models:
        x, p95, y = pooled.loc[m, "median_ms"], pooled.loc[m, "p95_ms"], cost.loc[m, "usd_per_1000_decisions"]
        ax.plot([x, p95], [y, y], color=MODEL_COLOURS[m], linewidth=2, solid_capstyle="round", zorder=1, alpha=0.6)
        ax.plot([x], [y], marker="o", markersize=13, color=MODEL_COLOURS[m], markeredgecolor=SURFACE, markeredgewidth=2, zorder=3)
        below = m == cheapest and len(models) > 1
        ax.annotate(f"{MODEL_NAMES[m]}\n{x:.0f} ms median, ${y:.3f}", (p95, y), xytext=(9, -4 if below else 0),
                    textcoords="offset points", ha="left", va="top" if below else "center", fontsize=11.5, color=INK2,
                    linespacing=1.2)
    ax.set_xlabel("Latency per decision, ms (dot: median; line: to the 95th percentile)")
    ax.set_ylabel("Cost per 1,000 decisions, USD")
    ax.set_xlim(0, max(pooled.p95_ms) * 1.5)
    ax.set_ylim(0, max(cost.usd_per_1000_decisions) * 1.6)
    ax.grid(axis="y", color=GRID, linewidth=1)
    _style(ax)
    n = int(pooled.n.iloc[0])
    return _finish(fig, out_dir / "speed_cost.png", title,
                   f"Client-side latency over one persistent connection from the UK, {n:,} calls per model, models interleaved. "
                   "Cost as billed by OpenRouter.", left=0.12, bottom=0.2)


def chart_aa_reweighting(out_dir, title) -> Path:
    scores = desk_aa.SCORES
    names = [n for n in ("Jev 1.14", "Gemini Decision 1", "Clef", "Drex Max v1.1") if n in scores]
    key = {"Jev 1.14": "jev", "Gemini Decision 1": "gemini", "Clef": "clef"}
    fig, ax = plt.subplots(figsize=(FIG_W, 3.9))
    for i, name in enumerate(names):
        colour = MODEL_COLOURS.get(key.get(name), MUTED)
        full = desk_aa.index(scores[name])
        without = desk_aa.index(scores[name], drop=desk_aa.KNOWLEDGE_AND_REASONING)
        ax.plot([full, without], [i, i], color=colour, linewidth=2, zorder=1)
        ax.plot([full], [i], marker="o", markersize=10, color=SURFACE, markeredgecolor=colour, markeredgewidth=2, zorder=2)
        ax.plot([without], [i], marker="o", markersize=11, color=colour, markeredgecolor=SURFACE, markeredgewidth=2, zorder=3)
        ax.annotate(f"{full:.1f}", (full, i), xytext=(-9, 0), textcoords="offset points", ha="right", va="center", fontsize=12, color=INK2)
        ax.annotate(f"{without:.1f}", (without, i), xytext=(9, 0), textcoords="offset points", ha="left", va="center", fontsize=12, color=INK2)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_ylim(len(names) - 0.5, -0.5)
    ax.set_xlim(55, 85)
    _style(ax)
    handles = [Line2D([], [], marker="o", color=SURFACE, markeredgecolor=INK2, markeredgewidth=2, markersize=9, linestyle="none"),
               Line2D([], [], marker="o", color=INK2, markersize=10, linestyle="none")]
    fig.legend(handles, ["AA Decision Index as published", "Without the knowledge and reasoning exams"], loc="lower right",
               bbox_to_anchor=(0.98, 0.075), ncol=2)
    return _finish(fig, out_dir / "aa_reweighting.png", title,
                   "Component scores from the 16 November snapshot, reweighted without AA-Omniscience-Decision and HLE-MultiChoice "
                   f"(30% of the index). On the reweighted index a gap between two models carries about ±{desk_aa.reweighted_gap_half_width(40):.1f} "
                   "points of sampling noise at a per-item sd of 40.", left=0.22, bottom=0.28)


def render_all(tables: dict, out_dir: Path | str) -> dict[str, str]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    heads = titles(tables)
    written = {
        "errors_at_half": chart_errors_at_half(tables, out_dir, heads["errors_at_half"]),
        "operating_points": chart_operating_points(tables, out_dir, heads["operating_points"]),
        "fooling": chart_fooling(tables, out_dir, heads["fooling"]),
        "rewording": chart_rewording(tables, out_dir, heads["rewording"]),
        "speed_cost": chart_speed_cost(tables, out_dir, heads["speed_cost"]),
        "aa_reweighting": chart_aa_reweighting(out_dir, heads["aa_reweighting"]),
    }
    manifest = {name: {"file": path.name, "title": heads[name],
                       "data": "results/desk/aa_reweighting_and_noise.md" if name == "aa_reweighting" else
                       {"errors_at_half": "accuracy.csv", "operating_points": "operating_points.csv", "fooling": "fooling.csv",
                        "rewording": "rewording.csv", "speed_cost": "speed.csv and cost.csv"}[name]}
                for name, path in written.items()}
    (out_dir / "charts.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8", newline="\n")
    return {name: str(path) for name, path in written.items()}


def load_tables(results_dir: Path | str) -> dict[str, pd.DataFrame]:
    results_dir = Path(results_dir)
    return {name: pd.read_csv(results_dir / f"{name}.csv") for name in TABLE_FILES}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results", type=Path, default=RESULTS)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)
    out = args.out or (args.results / "charts")
    written = render_all(load_tables(args.results), out)
    for name, path in written.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
