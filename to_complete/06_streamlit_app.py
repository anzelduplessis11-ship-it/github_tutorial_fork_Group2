from __future__ import annotations

from typing import Any, Dict


def build_streamlit_dashboard(visual_bundle: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare the data that a Streamlit app will render.

    Input contract:
    - visual_bundle["dataset_name"]: str
    - visual_bundle["metrics"]: dict
    - visual_bundle["figure_paths"]: list[str]
    - visual_bundle["chart_notes"]: list[str]
    - visual_bundle["sample_predictions"]: list[dict]

    Expected work:
    - build the layout for a Streamlit page
    - show the metrics
    - show the saved plots
    - show a small table of predictions

    Tip:
    - keep the page simple and visual first

    Output contract:
    - dataset_name: str
    - title: str
    - metrics: dict
    - figure_paths: list[str]
    - widgets: list[str]
    - sample_predictions: list[dict]
    """
    dataset_name = visual_bundle.get("dataset_name", "unknown_dataset")
    title = visual_bundle.get("title") or f"{dataset_name} Dashboard"
    metrics = visual_bundle.get("metrics", {})
    figure_paths = list(visual_bundle.get("figure_paths", []))
    chart_notes = list(visual_bundle.get("chart_notes", []))
    sample_predictions = list(visual_bundle.get("sample_predictions", []))

    # Describe the page layout as an ordered list of widgets. Keeping this as
    # plain strings makes the layout easy to inspect and easy for a Streamlit
    # script to loop over when it actually renders the page.
    widgets: list[str] = []
    widgets.append(f"title:{title}")
    widgets.append(f"header:Dataset - {dataset_name}")

    if metrics:
        widgets.append("subheader:Metrics")
        for name, value in metrics.items():
            widgets.append(f"metric:{name}={value}")
    else:
        widgets.append("info:No metrics available")

    if figure_paths:
        widgets.append("subheader:Charts")
        for path in figure_paths:
            widgets.append(f"image:{path}")
    else:
        widgets.append("info:No figures to display")

    for note in chart_notes:
        widgets.append(f"caption:{note}")

    if sample_predictions:
        widgets.append("subheader:Sample predictions")
        widgets.append(f"table:{len(sample_predictions)} rows")

    return {
        "dataset_name": dataset_name,
        "title": title,
        "metrics": metrics,
        "figure_paths": figure_paths,
        "widgets": widgets,
        "sample_predictions": sample_predictions,
    }
