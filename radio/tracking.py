"""Transport-neutral boundary for locally computed or authenticated SGP4 state.

Trust is provisioned by local integration code, never by a BLE request field.
This module does not compute or validate an orbit model.
"""


class TrackingInput:
    def __init__(self, safety):
        self.safety = safety
        self.trusted_sources = set()

    def provision(self, source: str):
        if not isinstance(source, str) or not source or len(source) > 128:
            raise ValueError("invalid locally provisioned tracking source")
        self.trusted_sources.add(source)

    def revoke(self, source: str):
        self.trusted_sources.discard(source)
        self.safety.tracking = None
        self.safety.inhibit("tracking-source-revoked")

    def update(self, source: str, rate: float, utc: float, site):
        try:
            if source not in self.trusted_sources:
                raise PermissionError("locally provisioned verified tracking source required")
            self.safety.tracking_update(rate, utc, site, verified=True)
            self.safety.inhibit("tracking-update-requires-new-lease")
        except (PermissionError, ValueError, TypeError):
            self.safety.tracking = None
            self.safety.inhibit("tracking-source-rejected")
            raise
