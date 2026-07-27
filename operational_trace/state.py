from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SelectionState:
    selection_key: str | None = None
    last_event_timestamp: int = -1


def reconcile_selection(
    *,
    click_timestamps: tuple[int | None, ...],
    selector_keys: tuple[str, ...],
    available_selection_keys: tuple[str, ...],
    current_state: SelectionState,
) -> SelectionState:
    available_key_set = set(available_selection_keys)
    selected_key = (
        current_state.selection_key
        if current_state.selection_key in available_key_set
        else None
    )

    candidates = tuple(
        (timestamp, selector_key)
        for timestamp, selector_key in zip(
            click_timestamps,
            selector_keys,
            strict=False,
        )
        if timestamp is not None
        and timestamp > current_state.last_event_timestamp
        and selector_key in available_key_set
    )
    if not candidates:
        return SelectionState(
            selection_key=selected_key,
            last_event_timestamp=current_state.last_event_timestamp,
        )

    event_timestamp, event_key = max(candidates, key=lambda item: item[0])
    return SelectionState(
        selection_key=None if event_key == selected_key else event_key,
        last_event_timestamp=event_timestamp,
    )
