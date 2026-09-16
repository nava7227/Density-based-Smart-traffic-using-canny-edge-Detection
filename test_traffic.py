import numpy as np
import pytest
from traffic import ROOT, analyze, detect_edges, green_seconds, read_gray, save_edges
from CannyEdgeDetector import CannyEdgeDetector

@pytest.mark.parametrize('ratio,expected',[(0,20),(50,20),(50.01,30),(75,30),(75.01,40),(85,40),(85.01,50),(89.99,50),(90,60),(120,60)])
def test_timing_boundaries(ratio,expected): assert green_seconds(ratio)==expected

@pytest.mark.parametrize('ratio',[-1,float('nan'),float('inf')])
def test_invalid_ratio(ratio):
    with pytest.raises(ValueError): green_seconds(ratio)

def test_flat_image_has_no_edges(): assert not detect_edges(np.zeros((20,20))).any()

def test_hysteresis_follows_chain_in_both_directions():
    detector=CannyEdgeDetector([])
    image=np.zeros((7,7),dtype=int); image[3,1]=255; image[3,2:6]=75
    assert np.all(detector.hysteresis(image)[3,1:6]==255)
    assert np.all(detector.hysteresis(np.fliplr(image))[3,1:6]==255)

def test_repeated_calls_do_not_accumulate():
    detector=CannyEdgeDetector([np.zeros((10,10))])
    assert len(detector.detect())==len(detector.detect())==1

def test_missing_and_corrupt_image(tmp_path):
    with pytest.raises(ValueError): read_gray(tmp_path/'missing.png')
    bad=tmp_path/'bad.png'; bad.write_text('not an image')
    with pytest.raises(ValueError): read_gray(bad)

def test_blank_reference_rejected(tmp_path):
    path=tmp_path/'blank.png'; save_edges(path,np.zeros((20,20),dtype=np.uint8))
    with pytest.raises(ValueError,match='no detectable edges'): analyze(ROOT/'images/A.png',path)

@pytest.mark.parametrize('name',['A','B','C','D','refrence'])
def test_supplied_images(name):
    r=analyze(ROOT/'images'/f'{name}.png')
    assert r.sample_edges.shape==r.reference_edges.shape
    assert set(np.unique(r.sample_edges)).issubset({0,255})
    assert r.reference_pixels>0 and np.isfinite(r.ratio)
    assert r.seconds in {20,30,40,50,60}
    if name=='refrence': assert r.ratio==100

def test_gui_import_has_no_window():
    import tkinter as tk
    import Main
    assert tk._default_root is None
