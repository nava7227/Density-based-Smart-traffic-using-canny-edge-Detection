"""Process all supplied samples without opening the desktop interface."""
import argparse
import csv
from pathlib import Path
from traffic import ROOT, DEFAULT_REFERENCE, analyze, save_edges

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'outputs')
    parser.add_argument('--reference',type=Path,default=DEFAULT_REFERENCE)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    rows=[]
    for name in ['A','B','C','D']:
        result=analyze(ROOT/'images'/f'{name}.png',args.reference)
        save_edges(args.output/f'{name}-edges.png',result.sample_edges)
        rows.append(dict(image=f'{name}.png',sample_pixels=result.sample_pixels,reference_pixels=result.reference_pixels,edge_ratio_percent=round(result.ratio,3),green_seconds=result.seconds))
    save_edges(args.output/'reference-edges.png',result.reference_edges)
    with (args.output/'results.csv').open('w',newline='',encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    for row in rows: print(row)
    print(f'Results saved to {args.output}')

if __name__=='__main__':main()
