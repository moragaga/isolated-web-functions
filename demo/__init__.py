from __future__ import annotations


def build_demo_layout(*args, **kwargs):
    from .build import build_demo_layout as builder

    return builder(*args, **kwargs)


def register_demo_callbacks(*args, **kwargs):
    from .callbacks import register_demo_callbacks as register

    return register(*args, **kwargs)


__all__ = ('build_demo_layout', 'register_demo_callbacks')
