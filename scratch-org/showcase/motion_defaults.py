"""#389: motion defaults for every demo block.

The demo pages are the source of truth for the CPE design library (build_demo_variants.py
harvests them), so applying motion here puts it on the pages AND in every preset an admin
loads from "Next Design". The point is to see how each effect reads against every design,
so entrance rotates through all five styles rather than defaulting to one.

Only ever applied where the block actually supports the effect; setting a property a block
ignores would show up as a preset key that does nothing.
"""

# Rotated by block index so a single page shows several, and the library covers all five
ENTRANCE_CYCLE = ["rise", "cascade", "wipe", "zoom", "blur"]
HOVER_CYCLE = ["lift", "trace", "ring", "tint"]

# Blocks that render card-like children, the only place a hover style is visible
HOVER_TYPES = {"cards", "pricing", "steps", "statsBar", "callout", "showcase", "table", "pills"}

# From the block type registry: these are the only types that declare the feature
SHINE_TYPES = {"cta"}
COUNT_UP_TYPES = {"statsBar", "showcase"}


def apply_motion(props, index):
    """Mutates and returns props, adding motion appropriate to its sectionType."""
    section_type = props.get("sectionType")
    if not section_type:
        return props

    # Callers pass an ordinal, but some pass a slug; hash anything non-numeric so the
    # rotation stays deterministic per block rather than throwing.
    try:
        i = int(index)
    except (TypeError, ValueError):
        i = sum(ord(c) for c in str(index))

    # Entrance rotates so every style appears across the set, including zoom and blur
    props["entrance"] = ENTRANCE_CYCLE[i % len(ENTRANCE_CYCLE)]

    if section_type in HOVER_TYPES:
        props.setdefault("hoverStyle", HOVER_CYCLE[i % len(HOVER_CYCLE)])

    # A drifting gradient needs a real gradient to drift; "off" is a value, not an absence
    if props.get("backgroundGradient") not in (None, "", "off"):
        props.setdefault("gradientDrift", True)

    if section_type in SHINE_TYPES:
        props.setdefault("shineSweep", True)

    if section_type in COUNT_UP_TYPES:
        props.setdefault("countUp", True)

    return props
