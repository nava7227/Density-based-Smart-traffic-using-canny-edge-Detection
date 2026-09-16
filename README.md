# Density-Based Smart Traffic Control System

An academic Python desktop prototype that uses Canny edge detection to compare traffic-image edge pixels with a reference image and suggest a green-signal duration.

**Author:** Nava Chaitanya Karella  
**Academic project:** January 2024 - October 2025  
**Stack:** Python, Tkinter, OpenCV, NumPy, SciPy, scikit-image, Matplotlib

## What it does

1. Lets the user choose a traffic image.
2. Converts it to grayscale and applies the custom Canny edge detector.
3. Compares the resulting white-pixel count with a reference edge image.
4. Displays a suggested green-signal duration of 20-60 seconds.

This is an image-based demonstration. It does not operate physical traffic lights or measure an exact vehicle count.

## Files

| File | Purpose |
| --- | --- |
| `Main.py` | Tkinter interface, image processing workflow, and timing logic |
| `CannyEdgeDetector.py` | Custom edge-detector implementation |
| `test_script.py`, `test1_module.py` | Supporting test scripts; inspect their inputs before running |
| `run.bat` | Windows launch helper |

## Local setup

The original sample/reference images are not included in the current repository. Prepare these inputs before launching the workflow.

1. Install Python with Tkinter support.
2. Create and activate a virtual environment.
3. Install the libraries used by the application:

```bash
python -m pip install numpy scipy scikit-image matplotlib opencv-python
```

4. Create a `gray` directory in the repository root.
5. Place the reference edge image at **`gray/refrence.png`** (the spelling matches the current code). Use a representative reference image with nonzero white pixels and comparable image dimensions/preprocessing.
6. Run from the repository root:

```bash
python Main.py
```

These setup notes reflect code inspection; a clean-environment run and compatible dependency versions still need verification.

## Using the interface

Click the controls in order:

1. **Upload Traffic Image**
2. **Image Preprocessing Using Canny Edge Detection**
3. **White Pixel Count**
4. **Calculate Green Signal Time Allocation**

Processing writes `gray/test.png`. The reference image remains at `gray/refrence.png`.

## Timing rule

The percentage is `(sample white pixels / reference white pixels) * 100`. It is an image-edge ratio, not a validated traffic occupancy percentage.

| Edge-pixel ratio | Suggested green time |
| --- | --- |
| 90% or higher | 60 seconds |
| Greater than 85%, below 90% | 50 seconds |
| Greater than 75%, up to 85% | 40 seconds |
| Greater than 50%, up to 75% | 30 seconds |
| 50% or lower | 20 seconds |

## Limitations and next improvements

- Add redistributable sample/reference images and a screenshot of the working interface.
- Add tested dependency versions and repeatable setup instructions.
- Validate missing files, cancelled selections, grayscale inputs, and a zero-pixel reference image.
- Enforce the processing order and correct the swapped sample/reference labels in the pixel-count dialog.
- Separate timing logic from the interface and test threshold boundaries.
- Evaluate sensitivity to lighting, shadows, camera angle, and image size using a documented dataset.

No benchmark accuracy or live-deployment performance is claimed.

## Contact

[Nava Chaitanya Karella on LinkedIn](https://www.linkedin.com/in/navakarella0027/)
