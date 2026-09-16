"""Launch the desktop demo with python Main.py."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from traffic import ROOT, DEFAULT_REFERENCE, analyze

class TrafficApp:
    def __init__(self, root):
        self.root = root
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.sample = None
        self.reference = DEFAULT_REFERENCE
        self.result = None
        self.future = None
        root.title('Traffic Image Analysis')
        root.geometry('760x470'); root.minsize(600,430)
        frame=ttk.Frame(root,padding=24); frame.pack(fill='both',expand=True)
        ttk.Label(frame,text='Traffic Image Analysis',font=('Segoe UI',20,'bold')).pack(anchor='w')
        ttk.Label(frame,text='Academic prototype: compare image edges and suggest a green-signal duration.',wraplength=650).pack(anchor='w',pady=(4,18))
        self.sample_label=ttk.Label(frame,text='No traffic image selected',wraplength=650)
        self.sample_label.pack(anchor='w')
        self.select_button=ttk.Button(frame,text='Choose traffic image',command=self.select_sample)
        self.select_button.pack(anchor='w',pady=(6,12))
        self.reference_label=ttk.Label(frame,text=f'Reference: {self.reference.name}',wraplength=650)
        self.reference_label.pack(anchor='w')
        self.reference_button=ttk.Button(frame,text='Choose reference image',command=self.select_reference)
        self.reference_button.pack(anchor='w',pady=(6,12))
        self.run_button=ttk.Button(frame,text='Analyze image',command=self.start,state='disabled')
        self.run_button.pack(anchor='w')
        self.status=ttk.Label(frame,text='Choose an image to begin.',wraplength=650)
        self.status.pack(anchor='w',pady=14)
        self.preview_button=ttk.Button(frame,text='Show edge comparison',command=self.preview,state='disabled')
        self.preview_button.pack(anchor='w')
        ttk.Label(frame,text='Edge density is not a vehicle count. This demo does not control real traffic signals.',wraplength=650).pack(anchor='w',pady=(18,0))
        root.protocol('WM_DELETE_WINDOW',self.close)

    def choose(self):
        return filedialog.askopenfilename(initialdir=ROOT/'images',filetypes=[('Images','*.png *.jpg *.jpeg *.bmp'),('All files','*.*')])

    def invalidate(self):
        self.result=None
        self.preview_button.configure(state='disabled')
        self.status.configure(text='Ready to analyze.' if self.sample else 'Choose an image to begin.')
        self.run_button.configure(state='normal' if self.sample else 'disabled')

    def select_sample(self):
        value=self.choose()
        if value:
            self.sample=Path(value); self.sample_label.configure(text=f'Traffic image: {self.sample.name}'); self.invalidate()

    def select_reference(self):
        value=self.choose()
        if value:
            self.reference=Path(value); self.reference_label.configure(text=f'Reference: {self.reference.name}'); self.invalidate()

    def start(self):
        if not self.sample or (self.future and not self.future.done()): return
        self.result=None
        for widget in (self.run_button,self.select_button,self.reference_button,self.preview_button): widget.configure(state='disabled')
        self.status.configure(text='Analyzing image...')
        self.future=self.executor.submit(analyze,self.sample,self.reference)
        self.root.after(80,self.poll)

    def poll(self):
        if not self.future.done():
            self.root.after(80,self.poll); return
        for widget in (self.run_button,self.select_button,self.reference_button): widget.configure(state='normal')
        try:
            self.result=self.future.result(); r=self.result
            self.status.configure(text=f'Sample edge pixels: {r.sample_pixels:,} | Reference edge pixels: {r.reference_pixels:,}\nEdge-density ratio: {r.ratio:.1f}% | Suggested green time: {r.seconds} seconds')
            self.preview_button.configure(state='normal')
        except Exception as error:
            self.status.configure(text='Analysis failed. Check the selected images and try again.')
            messagebox.showerror('Unable to analyze image',str(error))

    def preview(self):
        if self.result is None: return
        import matplotlib.pyplot as plt
        fig,axes=plt.subplots(1,2,figsize=(9,4))
        for ax,image,title in zip(axes,[self.result.sample_edges,self.result.reference_edges],['Traffic image edges','Reference image edges']):
            ax.imshow(image,cmap='gray',vmin=0,vmax=255); ax.set_title(title); ax.axis('off')
        fig.tight_layout(); plt.show()

    def close(self):
        self.executor.shutdown(wait=False,cancel_futures=True)
        self.root.destroy()

if __name__=='__main__':
    root=tk.Tk(); TrafficApp(root); root.mainloop()
