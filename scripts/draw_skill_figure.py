#!/usr/bin/env python3
"""Render the original, editable ScientistTwo skill overview (no external assets)."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/scientist-two-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
ROOT=Path(__file__).resolve().parents[1]
BG='#F6F8FC'; INK='#182B45'; MUTED='#50627A'; BLUE='#3866D5'; TEAL='#16847D'; PURPLE='#7855B8'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'svg.fonttype':'none'})
fig,ax=plt.subplots(figsize=(16,8.5));fig.patch.set_facecolor(BG);ax.set_facecolor(BG);ax.set_xlim(0,16);ax.set_ylim(0,8.5);ax.axis('off');fig.subplots_adjust(0,0,1,1)
def text(x,y,s,size=14,color=INK,weight='normal',**kw):ax.text(x,y,s,fontsize=size,color=color,fontweight=weight,va='center',**kw)
def box(x,y,w,h,face,edge='none',radius=.16,lw=1):
 p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={radius}',facecolor=face,edgecolor=edge,linewidth=lw);ax.add_patch(p);return p
def arrow(a,b,color=MUTED,style='-|>',lw=1.7,**kw):ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=15,linewidth=lw,color=color,**kw))
text(.7,7.96,'SCIENTIST TWO  /  RESEARCH SKILL',12,BLUE,'bold')
text(.7,7.36,'From a limitation to a defensible finding.',28,weight='bold')
text(.7,6.82,'Test ideas cheaply. Learn from failures. Make every claim traceable.',15,MUTED)
cols=[(.7,BLUE,'01  DISCOVER','Find a gap worth testing',[
 ('Limitation → hypothesis','Identify a baseline weakness.','Propose a mechanism that addresses it.'),
 ('Check the closest work','Compare distinct candidate ideas.','Record novelty evidence and uncertainty.')]),
 (5.72,TEAL,'02  EXPERIMENT','Earn the right to scale',[
 ('Reproduce → screen','Establish the subset baseline.','Evaluate candidates under aligned conditions.'),
 ('Scale the promising ideas','Good → full benchmark','Engineer → bounded repair   ·   Bad → prune')]),
 (10.74,PURPLE,'03  STRENGTHEN','Let evidence revise the story',[
 ('Ablate → refine','Isolate the sources of gain.','Keep revisions only after verification.'),
 ('Review → targeted experiments','Resolve criticism with new evidence.','Update the method, results and manuscript.')])]
for x,color,label,title,steps in cols:
 box(x,2.78,4.55,3.46,'white','#DEE5EF',.18)
 box(x,6.12,4.55,.12,color,radius=.04)
 text(x+.26,5.78,label,12,color,'bold');text(x+.26,5.31,title,16,weight='bold')
 for j,(head,line1,line2) in enumerate(steps):
  y=4.64-j*1.02
  ax.add_patch(Circle((x+.37,y),.1,facecolor=color,edgecolor='none'))
  text(x+.61,y,head,13.6,weight='bold');text(x+.26,y-.34,line1,12,MUTED);text(x+.26,y-.61,line2,11.5,MUTED)
arrow((5.3,4.54),(5.65,4.54),BLUE);arrow((10.32,4.54),(10.67,4.54),TEAL)
# A shared feedback lane, kept clear of cards and text.
arrow((13.02,2.71),(13.02,2.35),PURPLE)
ax.plot([13.02,11.9],[2.35,2.35],color=PURPLE,lw=1.7)
ax.plot([4.1,2.98],[2.35,2.35],color=PURPLE,lw=1.7)
arrow((2.98,2.35),(2.98,2.71),PURPLE)
box(4.1,2.08,7.8,.54,BG)
text(8,2.35,'Failures, ablations and reviews feed the next hypothesis',12.5,PURPLE,ha='center')
box(.7,.78,14.59,1.02,INK,radius=.16)
text(1.02,1.45,'THE CLAIM–ARTIFACT CHAIN',11,'#B7C9E4','bold')
text(1.02,1.06,'Scores ↔ outputs     ·     Task rules     ·     Verified references     ·     Method ↔ code',15,'white')
text(.7,.36,'Budget-bounded iteration  •  Preserve the best verified state  •  Report negative findings',11.5,MUTED)
text(15.29,.36,'Adapted from ScientistTwo · arXiv:2609.19644v1',9.5,MUTED,ha='right')
out=ROOT/'assets';out.mkdir(exist_ok=True)
fig.savefig(out/'scientist-two-skill-overview.png',dpi=240,facecolor=BG)
fig.savefig(out/'scientist-two-skill-overview.svg',facecolor=BG)
print(out/'scientist-two-skill-overview.png')
