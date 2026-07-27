(function (global) {
    'use strict';

    function normalizeTimestamp(value) {
        return Number.isFinite(value) ? value : -1;
    }

    function normalizeSelectionState(state) {
        return {
            selection_key: state && state.selection_key ? state.selection_key : null,
            last_event_timestamp: normalizeTimestamp(
                state && state.last_event_timestamp
            ),
        };
    }

    function resolveSelection(
        clickTimestamps,
        snapshot,
        selectorIds,
        currentState
    ) {
        const state = normalizeSelectionState(currentState);
        const availableKeys = new Set(
            snapshot && Array.isArray(snapshot.selectable_selection_keys)
                ? snapshot.selectable_selection_keys
                : snapshot && Array.isArray(snapshot.selection_keys)
                    ? snapshot.selection_keys
                    : []
        );
        let selectedKey = availableKeys.has(state.selection_key)
            ? state.selection_key
            : null;
        let selectedTimestamp = state.last_event_timestamp;
        let eventKey = null;

        (clickTimestamps || []).forEach(function (rawTimestamp, index) {
            const timestamp = normalizeTimestamp(rawTimestamp);
            const selectorId = (selectorIds || [])[index] || {};
            const selectionKey = selectorId.alarm || null;
            if (
                timestamp > selectedTimestamp
                && selectionKey
                && availableKeys.has(selectionKey)
            ) {
                selectedTimestamp = timestamp;
                eventKey = selectionKey;
            }
        });

        if (eventKey) {
            selectedKey = eventKey === selectedKey ? null : eventKey;
        }

        return {
            selection_key: selectedKey,
            last_event_timestamp: selectedTimestamp,
        };
    }

    function resolveRenderState(
        selectionState,
        snapshot,
        selectorIds,
        routeIds,
        markerIds
    ) {
        const state = normalizeSelectionState(selectionState);
        const availableKeys = new Set(
            snapshot && Array.isArray(snapshot.selectable_selection_keys)
                ? snapshot.selectable_selection_keys
                : snapshot && Array.isArray(snapshot.selection_keys)
                    ? snapshot.selection_keys
                    : []
        );
        const selectedKey = availableKeys.has(state.selection_key)
            ? state.selection_key
            : null;
        const selectedValue = selectedKey || '';
        const hasSelection = selectedKey ? 'true' : 'false';

        function selectionFlags(ids) {
            return (ids || []).map(function (id) {
                return id && id.alarm === selectedKey ? 'true' : 'false';
            });
        }

        const cardFlags = selectionFlags(selectorIds);
        return [
            selectedValue,
            hasSelection,
            cardFlags,
            cardFlags,
            selectionFlags(routeIds),
            selectionFlags(markerIds),
        ];
    }

    const namespace = global.dash_clientside = global.dash_clientside || {};
    namespace.operational_trace = namespace.operational_trace || {};
    namespace.operational_trace.update_selection = resolveSelection;
    namespace.operational_trace.render_selection = resolveRenderState;

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = {
            resolveSelection,
            resolveRenderState,
        };
    }
}(typeof window !== 'undefined' ? window : globalThis));
