from __future__ import annotations

from collections.abc import Sequence

Point = tuple[float, float]
Profile = tuple[Point, ...]

_PROFILE_PHASES: dict[float, Profile] = {
    0.0: (
        (0.45, 0.00),
        (0.46, 0.00),
        (0.47, 0.00),
        (0.48, 0.00),
        (0.49, 0.00),
        (0.50, 0.00),
        (0.51, 0.00),
        (0.52, 0.00),
        (0.53, 0.00),
        (0.54, 0.00),
        (0.55, 0.00),
    ),
    0.30: (
        (0.20, 0.00),
        (0.24, 0.04),
        (0.31, 0.11),
        (0.39, 0.20),
        (0.46, 0.28),
        (0.51, 0.30),
        (0.57, 0.27),
        (0.65, 0.19),
        (0.73, 0.10),
        (0.79, 0.03),
        (0.82, 0.00),
    ),
    0.65: (
        (0.07, 0.00),
        (0.12, 0.08),
        (0.21, 0.23),
        (0.32, 0.40),
        (0.43, 0.57),
        (0.51, 0.65),
        (0.59, 0.62),
        (0.69, 0.49),
        (0.80, 0.30),
        (0.89, 0.10),
        (0.94, 0.00),
    ),
    1.0: (
        (0.00, 0.00),
        (0.06, 0.10),
        (0.16, 0.28),
        (0.28, 0.50),
        (0.40, 0.73),
        (0.49, 0.92),
        (0.57, 0.88),
        (0.68, 0.72),
        (0.80, 0.47),
        (0.92, 0.17),
        (1.00, 0.00),
    ),
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def interpolate_profile(ratio: float) -> Profile:
    normalized_ratio = clamp(ratio, 0.0, 1.0)
    phase_keys = tuple(sorted(_PROFILE_PHASES))
    lower_key, upper_key = _resolve_phase_range(normalized_ratio, phase_keys)
    lower_profile = _PROFILE_PHASES[lower_key]
    upper_profile = _PROFILE_PHASES[upper_key]
    if lower_key == upper_key:
        return lower_profile
    factor = (normalized_ratio - lower_key) / (upper_key - lower_key)
    return tuple(
        (
            lower_x + (upper_x - lower_x) * factor,
            lower_height + (upper_height - lower_height) * factor,
        )
        for (lower_x, lower_height), (upper_x, upper_height) in zip(
            lower_profile,
            upper_profile,
            strict=True,
        )
    )


def scale_profile(
    profile: Sequence[Point],
    *,
    left: float,
    base_y: float,
    width: float,
    max_height: float,
) -> tuple[Point, ...]:
    return tuple(
        (left + normalized_x * width, base_y - normalized_height * max_height)
        for normalized_x, normalized_height in profile
    )


def build_smooth_closed_path(points: Sequence[Point]) -> str:
    if len(points) < 2:
        raise ValueError('A stockpile path requires at least two points')
    commands = [f'M {points[0][0]:.2f} {points[0][1]:.2f}']
    for index in range(len(points) - 1):
        previous = points[index - 1] if index > 0 else points[index]
        current = points[index]
        following = points[index + 1]
        next_point = points[index + 2] if index + 2 < len(points) else following
        control_1 = (
            current[0] + (following[0] - previous[0]) / 6.0,
            current[1] + (following[1] - previous[1]) / 6.0,
        )
        control_2 = (
            following[0] - (next_point[0] - current[0]) / 6.0,
            following[1] - (next_point[1] - current[1]) / 6.0,
        )
        commands.append(
            'C '
            f'{control_1[0]:.2f} {control_1[1]:.2f}, '
            f'{control_2[0]:.2f} {control_2[1]:.2f}, '
            f'{following[0]:.2f} {following[1]:.2f}'
        )
    commands.append('Z')
    return ' '.join(commands)


def profile_top_y(points: Sequence[Point]) -> float:
    if not points:
        raise ValueError('A stockpile profile must not be empty')
    return min(point[1] for point in points)


def _resolve_phase_range(ratio: float, phase_keys: Sequence[float]) -> tuple[float, float]:
    if ratio <= phase_keys[0]:
        return phase_keys[0], phase_keys[0]
    if ratio >= phase_keys[-1]:
        return phase_keys[-1], phase_keys[-1]
    for lower_key, upper_key in zip(phase_keys, phase_keys[1:], strict=False):
        if lower_key <= ratio <= upper_key:
            return lower_key, upper_key
    return phase_keys[-1], phase_keys[-1]
