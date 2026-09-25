# Adam Acquisition v7.0.2.1 — Camera Orientation & Self-Test Fix

- Corrected live preview so the user's left appears on the left and right appears on the right.
- Corrected captured pixels to match the preview instead of reversing after capture.
- Prevented double-mirroring on the captured-photo review.
- Fixed camera stability self-test aggregate `ok` calculation: expected safety flags (`external_network_accessed=false`, `real_camera_accessed=false`) no longer make the test fail.
- Camera/attachment separation and front/rear switching remain unchanged.
