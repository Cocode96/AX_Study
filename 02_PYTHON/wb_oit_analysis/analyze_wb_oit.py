from __future__ import annotations

import argparse
import colorsys
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ALPHA_MODE_NAMES = {0: "Pow", 1: "LinExp"}
DEPTH_MODE_NAMES = {0: "None", 1: "Exp"}

CATEGORY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("ice", ("ice", "frost", "snow", "freeze", "frozen", "glacier")),
    ("fire", ("fire", "flame", "burn", "blaze", "meteor", "lava")),
    ("lightning", ("lightning", "thunder", "electric", "spark", "shock")),
    ("dark", ("dark", "shadow", "fear", "ghost", "curse", "cichol")),
    ("holy_light", ("holy", "light", "heal", "resurrect", "glow")),
    ("magic_circle", ("magiccircle", "magic_circle", "rune", "circle", "ring", "round")),
    ("wind", ("wind", "tornado", "cyclone", "gust")),
    ("water", ("water", "aqua", "wave", "splash")),
    ("slash_trail", ("slash", "blade", "sword", "trail", "swing")),
    ("explosion", ("explosion", "explode", "burst", "bomb", "impact")),
    ("smoke_dust", ("smoke", "dust", "fog", "cloud")),
    ("music", ("bard", "melody", "symphony", "music", "note")),
    ("boss", ("glasgavelen", "gargoyle", "hellhound", "boss")),
)


def default_preset_dir() -> Path:
    code_root = Path(__file__).resolve().parents[3]
    return code_root / "Mabinogi-Project/Client/Bin/DataFiles/EffectPresets"


def flatten_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from flatten_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from flatten_strings(child)


def classify_effect(path: Path, data: dict[str, Any]) -> str:
    searchable = " ".join(
        [path.stem, str(data.get("GameObjectName", "")), *flatten_strings(data)]
    ).lower()
    searchable = re.sub(r"[^a-z0-9_]+", " ", searchable)

    for category, keywords in CATEGORY_RULES:
        if any(keyword in searchable for keyword in keywords):
            return category
    return "other"


def preset_type(path: Path) -> str:
    name = path.stem.lower()
    for prefix, label in (
        ("pointpreset", "point"),
        ("quadpreset", "quad"),
        ("meshpreset", "mesh"),
        ("trailpreset", "trail"),
    ):
        if name.startswith(prefix):
            return label
    return "unknown"


def collect_color_values(value: Any, key_path: tuple[str, ...] = ()) -> list[tuple[str, tuple[float, float, float]]]:
    colors: list[tuple[str, tuple[float, float, float]]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            colors.extend(collect_color_values(child, (*key_path, str(key))))
        return colors

    if isinstance(value, list):
        key_name = ".".join(key_path)
        is_color_key = any("color" in key.lower() for key in key_path)
        if is_color_key and len(value) in (3, 4) and all(isinstance(v, (int, float)) for v in value):
            rgb = tuple(float(v) for v in value[:3])
            if all(math.isfinite(channel) for channel in rgb):
                colors.append((key_name, rgb))
        else:
            for child in value:
                colors.extend(collect_color_values(child, key_path))
    return colors


def color_label(rgb: tuple[float, float, float] | None) -> tuple[str, float, float, float, str]:
    if rgb is None:
        return "texture_or_default", math.nan, math.nan, math.nan, "unknown"

    clipped = tuple(min(1.0, max(0.0, channel)) for channel in rgb)
    luminance = 0.2126 * clipped[0] + 0.7152 * clipped[1] + 0.0722 * clipped[2]
    hue, saturation, _ = colorsys.rgb_to_hsv(*clipped)

    if max(clipped) < 0.08:
        family = "black"
    elif min(clipped) > 0.92:
        family = "white"
    elif saturation < 0.12:
        family = "gray"
    else:
        degrees = hue * 360.0
        if degrees < 15 or degrees >= 345:
            family = "red"
        elif degrees < 45:
            family = "orange"
        elif degrees < 70:
            family = "yellow"
        elif degrees < 165:
            family = "green"
        elif degrees < 200:
            family = "cyan"
        elif degrees < 255:
            family = "blue"
        elif degrees < 290:
            family = "purple"
        elif degrees < 345:
            family = "magenta"
        else:
            family = "red"

    brightness = "dark" if luminance < 0.25 else "mid" if luminance < 0.65 else "bright"
    return family, *clipped, brightness


def representative_color(colors: list[tuple[str, tuple[float, float, float]]]) -> tuple[float, float, float] | None:
    if not colors:
        return None
    values = np.asarray([rgb for _, rgb in colors], dtype=float)
    return tuple(np.clip(values.mean(axis=0), 0.0, 1.0))


def is_engine_default_color(field: str, rgb: tuple[float, float, float]) -> bool:
    defaults = {
        "PointDesc.StartColor": (1.0, 1.0, 1.0),
        "PointDesc.EndColor": (1.0, 1.0, 1.0),
        "QuadDesc.ColorMin": (1.0, 1.0, 1.0),
        "QuadDesc.ColorMax": (1.0, 1.0, 1.0),
        "BloomColor": (1.0, 1.0, 1.0),
        "BloomColorPerMesh": (1.0, 1.0, 1.0),
        "GradientBrightColors": (1.0, 0.0, 0.0),
        "GradientDarkColors": (0.0, 0.0, 0.0),
    }
    expected = defaults.get(field)
    return expected is not None and all(
        math.isclose(actual, default, abs_tol=1e-6)
        for actual, default in zip(rgb, expected)
    )


def load_preset(path: Path, root: Path) -> dict[str, Any] | None:
    try:
        with path.open(encoding="utf-8-sig") as file:
            data = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"[skip] {path}: {error}")
        return None

    if not isinstance(data, dict) or not isinstance(data.get("WB_OIT"), dict):
        return None

    wb = data["WB_OIT"]
    colors = collect_color_values(data)
    custom_colors = [
        (field, rgb)
        for field, rgb in colors
        if not is_engine_default_color(field, rgb)
    ]
    rgb = representative_color(custom_colors)
    family, red, green, blue, brightness = color_label(rgb)
    alpha_mode = int(wb.get("AlphaMode", 0))
    depth_mode = int(wb.get("DepthMode", 0))

    return {
        "file": str(path.relative_to(root)),
        "preset_name": path.stem,
        "preset_type": preset_type(path),
        "category": classify_effect(path, data),
        "alpha_mode": alpha_mode,
        "alpha_formula": ALPHA_MODE_NAMES.get(alpha_mode, f"Unknown({alpha_mode})"),
        "depth_mode": depth_mode,
        "depth_formula": DEPTH_MODE_NAMES.get(depth_mode, f"Unknown({depth_mode})"),
        "mode_pair": f"{ALPHA_MODE_NAMES.get(alpha_mode, alpha_mode)} + {DEPTH_MODE_NAMES.get(depth_mode, depth_mode)}",
        "k_alpha": float(wb.get("kAlpha", 0.0)),
        "p_alpha": float(wb.get("pAlpha", 0.0)),
        "k_depth": float(wb.get("kDepth", 0.0)),
        "color_family": family,
        "brightness": brightness,
        "color_r": red,
        "color_g": green,
        "color_b": blue,
        "color_status": "custom_json" if custom_colors else "engine_default_or_texture",
        "color_source_count": len(custom_colors),
        "default_color_count": len(colors) - len(custom_colors),
        "color_fields": ";".join(sorted({name for name, _ in custom_colors})),
    }


def load_dataframe(root: Path) -> pd.DataFrame:
    rows = [row for path in root.rglob("*.json") if (row := load_preset(path, root)) is not None]
    if not rows:
        raise RuntimeError(f"WB_OIT 데이터가 있는 JSON을 찾지 못했습니다: {root}")
    return pd.DataFrame(rows)


def build_summary(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby(["category", "alpha_formula", "depth_formula"], dropna=False)
        .agg(
            preset_count=("preset_name", "size"),
            k_alpha_median=("k_alpha", "median"),
            p_alpha_median=("p_alpha", "median"),
            k_depth_median=("k_depth", "median"),
            known_color_ratio=("color_r", lambda values: values.notna().mean()),
        )
        .reset_index()
        .sort_values(["preset_count", "category"], ascending=[False, True])
    )


def save_dashboard(frame: pd.DataFrame, output: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), constrained_layout=True)
    fig.suptitle("Mabinogi Effect Preset WB-OIT Analysis", fontsize=17, fontweight="bold")

    mode_counts = frame["mode_pair"].value_counts().sort_values()
    mode_counts.plot.barh(ax=axes[0, 0], color="#2878B5")
    axes[0, 0].set_title("Preset count by weight mode")
    axes[0, 0].set_xlabel("Preset count")

    common_categories = frame["category"].value_counts().head(10).index
    box_data = [frame.loc[frame["category"] == category, "k_alpha"].to_numpy() for category in common_categories]
    axes[0, 1].boxplot(
        box_data,
        tick_labels=common_categories,
        orientation="horizontal",
        showfliers=False,
    )
    axes[0, 1].set_title("kAlpha distribution by effect category")
    axes[0, 1].set_xlabel("kAlpha")

    known = frame.dropna(subset=["color_r", "color_g", "color_b"])
    if known.empty:
        axes[1, 0].text(0.5, 0.5, "No explicit JSON colors", ha="center", va="center")
    else:
        point_colors = known[["color_r", "color_g", "color_b"]].to_numpy()
        for mode, marker in (("Pow", "o"), ("LinExp", "s")):
            subset = known[known["alpha_formula"] == mode]
            if subset.empty:
                continue
            indices = subset.index
            axes[1, 0].scatter(
                subset["p_alpha"], subset["k_alpha"],
                c=point_colors[known.index.get_indexer(indices)], marker=marker,
                edgecolors="#333333", linewidths=0.35, alpha=0.72, label=mode,
            )
        axes[1, 0].legend(title="Alpha mode")
    axes[1, 0].set_title("Alpha parameters colored by JSON color")
    axes[1, 0].set_xlabel("pAlpha")
    axes[1, 0].set_ylabel("kAlpha")

    table = pd.crosstab(frame["brightness"], frame["mode_pair"])
    image = axes[1, 1].imshow(table.to_numpy(), cmap="YlGnBu", aspect="auto")
    axes[1, 1].set_xticks(range(len(table.columns)), table.columns, rotation=25, ha="right")
    axes[1, 1].set_yticks(range(len(table.index)), table.index)
    axes[1, 1].set_title("Brightness class and mode pair")
    for row in range(table.shape[0]):
        for column in range(table.shape[1]):
            axes[1, 1].text(column, row, int(table.iloc[row, column]), ha="center", va="center")
    fig.colorbar(image, ax=axes[1, 1], label="Preset count")

    for axis in axes.flat:
        axis.grid(axis="x", alpha=0.2)
    fig.savefig(output, dpi=170)
    plt.close(fig)


def alpha_weight(alpha: np.ndarray, alpha_mode: int, k_alpha: float, p_alpha: float) -> np.ndarray:
    clipped = np.maximum(1e-3, np.clip(alpha, 0.0, 1.0))
    if alpha_mode == 0:
        return np.power(clipped, p_alpha) * k_alpha
    return 1.0 - np.exp(-clipped * k_alpha)


def save_weight_curves(frame: pd.DataFrame, output: Path) -> None:
    alpha = np.linspace(0.0, 1.0, 200)
    frequent = frame.groupby(["alpha_mode", "k_alpha", "p_alpha"]).size().nlargest(8)
    fig, axis = plt.subplots(figsize=(12, 7), constrained_layout=True)

    for (mode, k_alpha, p_alpha), count in frequent.items():
        label = f"{ALPHA_MODE_NAMES.get(mode, mode)} k={k_alpha:g}, p={p_alpha:g} (n={count})"
        axis.plot(alpha, alpha_weight(alpha, mode, k_alpha, p_alpha), linewidth=2, label=label)

    axis.set_title("Most frequently used WB-OIT alpha weight curves")
    axis.set_xlabel("Input alpha")
    axis.set_ylabel("Alpha-side weight")
    axis.grid(alpha=0.25)
    axis.legend(fontsize=9)
    fig.savefig(output, dpi=170)
    plt.close(fig)


def print_findings(frame: pd.DataFrame) -> None:
    print(f"Analyzed presets: {len(frame):,}")
    print(f"Custom JSON color: {frame['color_r'].notna().sum():,}")
    print(f"Engine default or texture color: {frame['color_r'].isna().sum():,}")
    print("\nMode pairs")
    print(frame["mode_pair"].value_counts().to_string())
    print("\nTop categories")
    print(frame["category"].value_counts().head(12).to_string())
    print("\nMost common parameter sets")
    columns = ["alpha_formula", "depth_formula", "k_alpha", "p_alpha", "k_depth"]
    print(frame.value_counts(columns).head(12).to_string())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze WB-OIT settings in EffectPreset JSON files.")
    parser.add_argument("--preset-dir", type=Path, default=default_preset_dir())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("output"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    preset_dir = args.preset_dir.resolve()
    output_dir = args.output_dir.resolve()
    if not preset_dir.is_dir():
        raise SystemExit(f"EffectPresets 폴더를 찾을 수 없습니다: {preset_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    frame = load_dataframe(preset_dir)
    summary = build_summary(frame)

    frame.to_csv(output_dir / "wb_oit_presets.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(output_dir / "wb_oit_summary.csv", index=False, encoding="utf-8-sig")
    save_dashboard(frame, output_dir / "wb_oit_dashboard.png")
    save_weight_curves(frame, output_dir / "wb_oit_weight_curves.png")
    print_findings(frame)
    print(f"\nOutput: {output_dir}")


if __name__ == "__main__":
    main()
