(function (global) {
    'use strict';

    const PREVIEW_TONE_PRIORITY = Object.freeze({
        critical: 0,
        warning: 1,
        neutral: 2,
    });
    const controllers = new Map();
    let reconcileQueued = false;

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

    function normalizeNonNegativeInteger(value, fallback) {
        const parsed = Number.parseInt(value, 10);
        return Number.isFinite(parsed) && parsed >= 0 ? parsed : fallback;
    }

    function normalizePositiveInteger(value, fallback) {
        const parsed = Number.parseInt(value, 10);
        return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
    }

    function resolvePreviewConfig(moduleElement) {
        const dataset = moduleElement ? moduleElement.dataset : {};
        return {
            enabled: dataset.previewEnabled !== 'false',
            revealMs: normalizePositiveInteger(dataset.previewRevealMs, 4000),
            holdMs: normalizePositiveInteger(dataset.previewHoldMs, 20000),
            fadeMs: normalizePositiveInteger(dataset.previewFadeMs, 3000),
            betweenMs: normalizeNonNegativeInteger(dataset.previewBetweenMs, 250),
            cyclePauseMs: normalizeNonNegativeInteger(
                dataset.previewCyclePauseMs,
                1500
            ),
            maxCycleSize: normalizePositiveInteger(
                dataset.previewMaxCycleSize,
                6
            ),
            keepSingleVisible: dataset.previewKeepSingleVisible !== 'false',
            orderStrategy: dataset.previewOrderStrategy || 'priority',
        };
    }

    function resolveTonePriority(tone) {
        return Object.hasOwn(PREVIEW_TONE_PRIORITY, tone)
            ? PREVIEW_TONE_PRIORITY[tone]
            : PREVIEW_TONE_PRIORITY.neutral;
    }

    function normalizePreviewCandidates(
        records,
        maxCycleSize,
        orderStrategy
    ) {
        const unique = new Map();
        (records || []).forEach(function (record, index) {
            if (!record || record.active === false) {
                return;
            }
            const selectionKey = record.selectionKey || null;
            const previewKey = record.previewKey || null;
            if (!selectionKey || !previewKey || unique.has(previewKey)) {
                return;
            }
            const tone = record.tone || 'neutral';
            const position = Number.parseFloat(record.position);
            unique.set(previewKey, {
                selectionKey,
                previewKey,
                tone,
                priority: resolveTonePriority(tone),
                order: Number.isFinite(record.order) ? record.order : index,
                position: Number.isFinite(position) ? position : index,
                sourceIndex: index,
            });
        });
        const candidates = Array.from(unique.values());
        candidates.sort(function (left, right) {
            if (orderStrategy === 'left-to-right') {
                return (
                    left.position - right.position
                    || left.order - right.order
                    || left.priority - right.priority
                    || left.sourceIndex - right.sourceIndex
                );
            }
            return (
                left.priority - right.priority
                || left.order - right.order
                || left.position - right.position
                || left.sourceIndex - right.sourceIndex
            );
        });
        return candidates.slice(0, maxCycleSize);
    }

    function resolveNextPreviewCandidate(candidates, completedPreviewKeys) {
        const completed = completedPreviewKeys instanceof Set
            ? completedPreviewKeys
            : new Set(completedPreviewKeys || []);
        return (candidates || []).find(function (candidate) {
            return !completed.has(candidate.previewKey);
        }) || null;
    }

    function resolvePreviewPlan(
        candidates,
        completedPreviewKeys,
        keepSingleVisible
    ) {
        if (!candidates || candidates.length === 0) {
            return {mode: 'idle', candidate: null};
        }
        if (keepSingleVisible && candidates.length === 1) {
            return {mode: 'steady', candidate: candidates[0]};
        }
        const candidate = resolveNextPreviewCandidate(
            candidates,
            completedPreviewKeys
        );
        if (candidate) {
            return {mode: 'cycle', candidate};
        }
        return {mode: 'cycle-complete', candidate: null};
    }

    function resolveCompletedPreviewKeysThroughSelection(
        candidates,
        selectedSelectionKey
    ) {
        const completed = new Set();
        const selectedIndex = (candidates || []).findIndex(function (candidate) {
            return candidate.selectionKey === selectedSelectionKey;
        });
        if (selectedIndex < 0) {
            return completed;
        }
        candidates.slice(0, selectedIndex + 1).forEach(function (candidate) {
            completed.add(candidate.previewKey);
        });
        return completed;
    }

    function shouldKeepActivePreview(
        activePreviewKey,
        candidates,
        hasManualSelection
    ) {
        if (!activePreviewKey || hasManualSelection) {
            return false;
        }
        return (candidates || []).some(function (candidate) {
            return candidate.previewKey === activePreviewKey;
        });
    }

    function collectPreviewCandidates(moduleElement, maxCycleSize, orderStrategy) {
        const routesBySelectionKey = new Map();
        moduleElement
            .querySelectorAll('.operational-trace__route')
            .forEach(function (route) {
                const selectionKey = route.dataset.alarmOccurrenceId;
                if (selectionKey) {
                    routesBySelectionKey.set(selectionKey, route);
                }
            });

        const records = Array.from(
            moduleElement.querySelectorAll('.operational-alarm-card')
        ).map(function (card, index) {
            const selectionKey = card.dataset.alarmOccurrenceId || null;
            const route = routesBySelectionKey.get(selectionKey);
            return {
                selectionKey,
                previewKey: route
                    ? route.dataset.alarmPreviewKey
                    : card.dataset.alarmPreviewKey,
                tone: card.dataset.alarmTone || 'neutral',
                order: Number.parseInt(card.dataset.alarmOrder, 10),
                position: route
                    ? route.dataset.alarmPreviewPosition
                    : index,
                active: card.dataset.rotationActive !== 'false' && Boolean(route),
                index,
            };
        });
        return normalizePreviewCandidates(
            records,
            maxCycleSize,
            orderStrategy || 'priority'
        );
    }

    class PreviewController {
        constructor(moduleElement) {
            this.moduleElement = moduleElement;
            this.scopeId = moduleElement.dataset.operationalTraceScope;
            this.active = null;
            this.completedPreviewKeys = new Set();
            this.manualSelectionKey = null;
            this.timerId = null;
            this.timerGeneration = 0;
            this.destroyed = false;
        }

        updateModule(moduleElement) {
            this.moduleElement = moduleElement;
        }

        destroy() {
            this.destroyed = true;
            this.clearTimer();
            this.clearDomPreview();
        }

        reconcile() {
            if (this.destroyed || !this.moduleElement.isConnected) {
                return;
            }
            const config = resolvePreviewConfig(this.moduleElement);
            const root = this.resolveRoot();
            if (!config.enabled || !root) {
                this.cancelActive(false);
                this.clearTimer();
                return;
            }
            const hasManualSelection = root.dataset.hasSelection === 'true';
            const candidates = collectPreviewCandidates(
                this.moduleElement,
                config.maxCycleSize,
                config.orderStrategy
            );
            this.pruneCompleted(candidates);

            if (hasManualSelection) {
                const selectedSelectionKey = root.dataset.selectedAlarmId || null;
                if (
                    selectedSelectionKey
                    && selectedSelectionKey !== this.manualSelectionKey
                ) {
                    this.completedPreviewKeys = (
                        resolveCompletedPreviewKeysThroughSelection(
                            candidates,
                            selectedSelectionKey
                        )
                    );
                }
                this.manualSelectionKey = selectedSelectionKey;
                this.cancelActive(false);
                this.clearTimer();
                return;
            }

            const manualSelectionEnded = this.manualSelectionKey !== null;
            this.manualSelectionKey = null;

            if (config.keepSingleVisible && candidates.length === 1) {
                this.ensureSteadyPreview(candidates[0]);
                return;
            }

            if (this.active && this.active.phase === 'steady') {
                this.cancelActive(false);
                this.clearTimer();
            }

            if (this.active) {
                const keepActive = shouldKeepActivePreview(
                    this.active.previewKey,
                    candidates,
                    false
                );
                if (!keepActive) {
                    this.cancelActive(false);
                    this.scheduleNext(config.betweenMs);
                    return;
                }
                this.applyActiveToDom();
                return;
            }

            if (!this.timerId) {
                this.scheduleNext(manualSelectionEnded ? config.betweenMs : 0);
            }
        }

        resolveRoot() {
            return this.moduleElement.querySelector('.operational-trace');
        }

        readCandidates(config) {
            return collectPreviewCandidates(
                this.moduleElement,
                config.maxCycleSize,
                config.orderStrategy
            );
        }

        pruneCompleted(candidates) {
            const availableKeys = new Set(
                candidates.map(function (candidate) {
                    return candidate.previewKey;
                })
            );
            Array.from(this.completedPreviewKeys).forEach((previewKey) => {
                if (!availableKeys.has(previewKey)) {
                    this.completedPreviewKeys.delete(previewKey);
                }
            });
        }

        ensureSteadyPreview(candidate) {
            const alreadyActive = this.active
                && this.active.previewKey === candidate.previewKey
                && this.active.phase === 'steady';
            this.clearTimer();
            this.completedPreviewKeys.clear();
            if (!alreadyActive) {
                this.cancelActive(false);
                this.active = {
                    selectionKey: candidate.selectionKey,
                    previewKey: candidate.previewKey,
                    phase: 'steady',
                };
            }
            this.applyActiveToDom();
        }

        scheduleNext(delayMs) {
            this.setTimer(() => this.startNext(), delayMs);
        }

        startNext() {
            if (this.destroyed || !this.moduleElement.isConnected) {
                return;
            }
            const config = resolvePreviewConfig(this.moduleElement);
            const root = this.resolveRoot();
            if (
                !config.enabled
                || !root
                || root.dataset.hasSelection === 'true'
            ) {
                return;
            }
            const candidates = this.readCandidates(config);
            this.pruneCompleted(candidates);
            if (!candidates.length) {
                this.clearDomPreview();
                return;
            }
            const plan = resolvePreviewPlan(
                candidates,
                this.completedPreviewKeys,
                config.keepSingleVisible
            );
            if (plan.mode === 'steady') {
                this.ensureSteadyPreview(plan.candidate);
                return;
            }
            if (plan.mode === 'cycle-complete') {
                this.completedPreviewKeys.clear();
                this.scheduleNext(config.cyclePauseMs);
                return;
            }
            if (plan.mode === 'idle') {
                this.clearDomPreview();
                return;
            }
            this.startPreview(plan.candidate, config);
        }

        startPreview(candidate, config) {
            this.active = {
                selectionKey: candidate.selectionKey,
                previewKey: candidate.previewKey,
                phase: 'reveal',
            };
            this.applyActiveToDom(true);
            this.setTimer(() => this.enterHold(config), config.revealMs);
        }

        enterHold(config) {
            if (!this.activeStillValid(config)) {
                return;
            }
            this.active.phase = 'hold';
            this.applyActiveToDom();
            this.setTimer(() => this.enterFade(config), config.holdMs);
        }

        enterFade(config) {
            if (!this.activeStillValid(config)) {
                return;
            }
            this.active.phase = 'fade';
            this.applyActiveToDom();
            this.setTimer(() => this.finishPreview(config), config.fadeMs);
        }

        finishPreview(config) {
            if (!this.active) {
                return;
            }
            this.completedPreviewKeys.add(this.active.previewKey);
            this.cancelActive(false);
            this.scheduleNext(config.betweenMs);
        }

        activeStillValid(config) {
            if (!this.active) {
                return false;
            }
            const root = this.resolveRoot();
            const candidates = this.readCandidates(config);
            const valid = root
                && root.dataset.hasSelection !== 'true'
                && shouldKeepActivePreview(
                    this.active.previewKey,
                    candidates,
                    false
                );
            if (!valid) {
                this.cancelActive(false);
                this.scheduleNext(config.betweenMs);
                return false;
            }
            return true;
        }

        applyActiveToDom(restartReveal) {
            if (!this.active) {
                return;
            }
            const active = this.active;
            const root = this.resolveRoot();
            if (!root) {
                return;
            }
            this.clearDomPreviewNodes(active.previewKey);
            root.dataset.previewAlarmId = active.selectionKey;
            root.dataset.hasPreview = 'true';
            root.dataset.previewPhase = active.phase;

            const routes = this.moduleElement.querySelectorAll(
                '.operational-trace__route'
            );
            routes.forEach(function (route) {
                if (route.dataset.alarmPreviewKey !== active.previewKey) {
                    return;
                }
                if (restartReveal && active.phase === 'reveal') {
                    route.dataset.previewing = 'false';
                    route.dataset.previewPhase = 'idle';
                    void route.offsetWidth;
                }
                route.dataset.previewing = 'true';
                route.dataset.previewPhase = active.phase;
            });

            this.moduleElement
                .querySelectorAll('.operational-trace__marker')
                .forEach(function (marker) {
                    if (marker.dataset.alarmPreviewKey !== active.previewKey) {
                        return;
                    }
                    if (restartReveal && active.phase === 'reveal') {
                        marker.dataset.previewing = 'false';
                        marker.dataset.previewPhase = 'idle';
                        void marker.offsetWidth;
                    }
                    marker.dataset.previewing = 'true';
                    marker.dataset.previewPhase = active.phase;
                });
        }

        clearDomPreviewNodes(activePreviewKey) {
            this.moduleElement
                .querySelectorAll(
                    ".operational-trace__route[data-previewing='true'], "
                    + ".operational-trace__marker[data-previewing='true']"
                )
                .forEach(function (element) {
                    if (element.dataset.alarmPreviewKey === activePreviewKey) {
                        return;
                    }
                    element.dataset.previewing = 'false';
                    element.dataset.previewPhase = 'idle';
                });
        }

        clearDomPreview() {
            const root = this.resolveRoot();
            if (root) {
                root.dataset.previewAlarmId = '';
                root.dataset.hasPreview = 'false';
                root.dataset.previewPhase = 'idle';
            }
            this.moduleElement
                .querySelectorAll(
                    ".operational-trace__route[data-previewing='true'], "
                    + ".operational-trace__marker[data-previewing='true']"
                )
                .forEach(function (element) {
                    element.dataset.previewing = 'false';
                    element.dataset.previewPhase = 'idle';
                });
        }

        cancelActive(markCompleted) {
            if (markCompleted && this.active) {
                this.completedPreviewKeys.add(this.active.previewKey);
            }
            this.active = null;
            this.clearDomPreview();
        }

        setTimer(callback, delayMs) {
            this.clearTimer();
            const generation = ++this.timerGeneration;
            this.timerId = global.setTimeout(() => {
                if (this.destroyed || generation !== this.timerGeneration) {
                    return;
                }
                this.timerId = null;
                callback();
            }, Math.max(0, delayMs));
        }

        clearTimer() {
            this.timerGeneration += 1;
            if (this.timerId !== null) {
                global.clearTimeout(this.timerId);
                this.timerId = null;
            }
        }
    }

    function reconcileControllers() {
        reconcileQueued = false;
        if (typeof document === 'undefined') {
            return;
        }
        const presentScopes = new Set();
        document
            .querySelectorAll('[data-operational-trace-scope]')
            .forEach(function (moduleElement) {
                const scopeId = moduleElement.dataset.operationalTraceScope;
                if (!scopeId) {
                    return;
                }
                presentScopes.add(scopeId);
                let controller = controllers.get(scopeId);
                if (!controller) {
                    controller = new PreviewController(moduleElement);
                    controllers.set(scopeId, controller);
                } else {
                    controller.updateModule(moduleElement);
                }
                controller.reconcile();
            });

        Array.from(controllers.entries()).forEach(function (entry) {
            const scopeId = entry[0];
            const controller = entry[1];
            if (!presentScopes.has(scopeId)) {
                controller.destroy();
                controllers.delete(scopeId);
            }
        });
    }

    function queueControllerReconciliation() {
        if (reconcileQueued) {
            return;
        }
        reconcileQueued = true;
        Promise.resolve().then(reconcileControllers);
    }

    function startPreviewRuntime() {
        if (typeof document === 'undefined' || !document.body) {
            return;
        }
        queueControllerReconciliation();
        const observer = new MutationObserver(queueControllerReconciliation);
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: [
                'data-has-selection',
                'data-selected-alarm-id',
                'data-rotation-active',
                'data-alarm-occurrence-id',
                'data-alarm-preview-key',
            ],
        });
    }

    const namespace = global.dash_clientside = global.dash_clientside || {};
    namespace.operational_trace = namespace.operational_trace || {};
    namespace.operational_trace.update_selection = resolveSelection;
    namespace.operational_trace.render_selection = resolveRenderState;

    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', startPreviewRuntime, {
                once: true,
            });
        } else {
            startPreviewRuntime();
        }
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = {
            normalizePreviewCandidates,
            resolveCompletedPreviewKeysThroughSelection,
            resolveNextPreviewCandidate,
            resolvePreviewConfig,
            resolvePreviewPlan,
            resolveRenderState,
            resolveSelection,
            shouldKeepActivePreview,
        };
    }
}(typeof window !== 'undefined' ? window : globalThis));
