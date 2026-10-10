"""Complete residual digital signal links on a conservative two-layer routing grid.
KiCad DRC remains authoritative; this is not electrical/current qualification.
"""
import argparse, heapq, json, math, pathlib, subprocess, pcbnew
P=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--kicad-root',required=True);args=parser.parse_args()
b=pcbnew.LoadBoard(str(P/'cm5-guard-A.kicad_pcb'))
S=.15; W=1934; H=1634; N=W*H
layers=[pcbnew.F_Cu,pcbnew.B_Cu]
def mm(v):return pcbnew.ToMM(v)
def pos(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
def cell(x,y):return round(y/S)*W+round(x/S)
def xy(c):return (c%W*S,c//W*S)
def rect(mask,x1,y1,x2,y2):
 for y in range(max(0,math.floor(y1/S)),min(H,math.ceil(y2/S)+1)):
  a=y*W+max(0,math.floor(x1/S));z=y*W+min(W,math.ceil(x2/S)+1);mask[a:z]=b'\1'*(z-a)
def capsule(mask,x1,y1,x2,y2,r):
 dx=x2-x1;dy=y2-y1;ll=dx*dx+dy*dy
 for y in range(max(0,math.floor((min(y1,y2)-r)/S)),min(H,math.ceil((max(y1,y2)+r)/S)+1)):
  yy=y*S
  if abs(dy)>1e-8:
   tx=x1+dx*(yy-y1)/dy;span=r*math.sqrt(ll)/abs(dy)+S
   lo=max(min(x1,x2)-r,tx-span);hi=min(max(x1,x2)+r,tx+span)
  else:lo=min(x1,x2)-r;hi=max(x1,x2)+r
  for x in range(max(0,math.floor(lo/S)),min(W,math.ceil(hi/S)+1)):
   xx=x*S;t=max(0,min(1,((xx-x1)*dx+(yy-y1)*dy)/ll)) if ll else 0
   if (xx-x1-t*dx)**2+(yy-y1-t*dy)**2<=r*r:mask[y*W+x]=1

def route(netname,start,end,start_layer,end_layer):
 net=b.GetNetsByName()[netname];masks=[bytearray(N),bytearray(N)];vm=bytearray(N)
 for mask in masks+[vm]:
  rect(mask,0,0,290,1);rect(mask,0,0,1,245);rect(mask,289,0,290,245);rect(mask,0,244,290,245)
 for f in b.GetFootprints():
  for p in f.Pads():
   box=p.GetBoundingBox();x1=mm(box.GetX());y1=mm(box.GetY());x2=mm(box.GetRight());y2=mm(box.GetBottom())
   for i,ly in enumerate(layers):
    if p.IsOnLayer(ly) and p.GetNetCode()!=net.GetNetCode():rect(masks[i],x1-.3,y1-.3,x2+.3,y2+.3)
   if any(p.IsOnLayer(ly) for ly in layers):rect(vm,x1-.5,y1-.5,x2+.5,y2+.5)
 for t in b.GetTracks():
  a=t.GetStart();z=t.GetEnd();x1,y1,x2,y2=mm(a.x),mm(a.y),mm(z.x),mm(z.y)
  via=isinstance(t,pcbnew.PCB_VIA);width=mm(t.GetWidth(pcbnew.F_Cu) if via else t.GetWidth())
  affected=[0,1] if via else [layers.index(t.GetLayer())]
  if t.GetNetCode()!=net.GetNetCode():
   for i in affected:capsule(masks[i],x1,y1,x2,y2,width/2+.3)
   capsule(vm,x1,y1,x2,y2,width/2+.5)
  elif via:capsule(vm,x1,y1,x2,y2,.5)
 sc=cell(*start);ec=cell(*end);ss=sc+start_layer*N;es=ec+end_layer*N
 for c,ly in [(sc,start_layer),(ec,end_layer)]:masks[ly][c]=0
 ex,ey=ec%W,ec//W
 def heuristic(state):
  c=state%N;dx=abs(c%W-ex);dy=abs(c//W-ey);return 10*max(dx,dy)+4*min(dx,dy)
 queue=[(heuristic(ss),0,ss)];cost={ss:0};parent={};visited=0
 directions=[(-1,0,10),(1,0,10),(0,-1,10),(0,1,10),(-1,-1,14),(1,-1,14),(-1,1,14),(1,1,14)]
 while queue:
  _,g,state=heapq.heappop(queue)
  if cost.get(state)!=g:continue
  if state==es:break
  visited+=1;c=state%N;ly=state//N;x=c%W;y=c//W;mask=masks[ly]
  for dx,dy,w in directions:
   nx=x+dx;ny=y+dy
   if nx<0 or nx>=W or ny<0 or ny>=H:continue
   nc=ny*W+nx
   if mask[nc] or (dx and dy and (mask[c+dx] or mask[c+dy*W])):continue
   ns=nc+ly*N;ng=g+w
   if ng<cost.get(ns,10**10):cost[ns]=ng;parent[ns]=state;heapq.heappush(queue,(ng+heuristic(ns),ng,ns))
  if not vm[c] and not masks[1-ly][c]:
   ns=c+(1-ly)*N;ng=g+60
   if ng<cost.get(ns,10**10):cost[ns]=ng;parent[ns]=state;heapq.heappush(queue,(ng+heuristic(ns),ng,ns))
 else:raise RuntimeError('No conservative path: '+netname)
 path=[es]
 while path[-1]!=ss:path.append(parent[path[-1]])
 path.reverse();compact=[path[0]]
 for i in range(1,len(path)-1):
  if path[i]-path[i-1]!=path[i+1]-path[i]:compact.append(path[i])
 compact.append(path[-1])
 def addtrack(a,z,ly):
  if a==z:return
  t=pcbnew.PCB_TRACK(b);t.SetStart(pos(*a));t.SetEnd(pos(*z));t.SetNet(net);t.SetLayer(layers[ly]);t.SetWidth(pcbnew.FromMM(.2));b.Add(t)
 addtrack(start,xy(sc),start_layer)
 for a,z in zip(compact,compact[1:]):
  if a//N==z//N:addtrack(xy(a%N),xy(z%N),a//N)
  else:
   t=pcbnew.PCB_VIA(b);t.SetPosition(pos(*xy(a%N)));t.SetViaType(pcbnew.VIATYPE_THROUGH);t.SetLayerPair(*layers);t.SetWidth(pcbnew.FromMM(.6));t.SetDrill(pcbnew.FromMM(.3));t.SetNet(net);b.Add(t)
 addtrack(xy(ec),end,end_layer)
 print(netname,'states',visited,'segments',len(compact)-1)
cli=pathlib.Path(args.kicad_root)/'bin'/'kicad-cli.exe'
audit=[]
for attempt in range(5):
 pcbnew.SaveBoard(str(P/'cm5-guard-A.kicad_pcb'),b)
 subprocess.run([str(cli),'pcb','drc','--schematic-parity','--all-track-errors','--severity-all','--refill-zones','--save-board','--format','json','-o',str(P/'reports'/'drc.json'),str(P/'cm5-guard-A.kicad_pcb')],check=True)
 drc=json.loads((P/'reports'/'drc.json').read_text())
 if drc['violations'] or drc['schematic_parity']:raise RuntimeError('Non-routing DRC/parity issue; manual correction required')
 if not drc['unconnected_items']:break
 if attempt==4 or len(drc['unconnected_items'])>20:raise RuntimeError('Residual-routing bound exceeded')
 b=pcbnew.LoadBoard(str(P/'cm5-guard-A.kicad_pcb'))
 items={x.m_Uuid.AsString():x for x in b.GetTracks()}
 for f in b.GetFootprints():items.update({x.m_Uuid.AsString():x for x in f.Pads()})
 for issue in drc['unconnected_items']:
  left,right=[items[x['uuid']] for x in issue['items']]
  net=left.GetNetname()
  if net!=right.GetNetname() or not net:raise RuntimeError('Ambiguous missing connection')
  if any(key in net for key in ['BAT_POS','BAT_FUSED','BAT_PROTECTED','BRANCH_FUSED','GND_','VMOT','_M1','_M2','V3V3','_5V','EMI_','RF_']):raise RuntimeError('Power/RF routing requires manual qualification-aware correction: '+net)
  def ends(item):
   if isinstance(item,pcbnew.PAD) or isinstance(item,pcbnew.PCB_VIA):return [item.GetPosition()]
   return [item.GetStart(),item.GetEnd()]
  aa,zz=min(((a,z) for a in ends(left) for z in ends(right)),key=lambda pair:(pair[0].x-pair[1].x)**2+(pair[0].y-pair[1].y)**2)
  def layer(item):return 1 if isinstance(item,pcbnew.PAD) and item.IsOnLayer(pcbnew.B_Cu) else layers.index(item.GetLayer())
  route(net,(mm(aa.x),mm(aa.y)),(mm(zz.x),mm(zz.y)),layer(left),layer(right))
  audit.append({'net':net,'start_mm':[mm(aa.x),mm(aa.y)],'end_mm':[mm(zz.x),mm(zz.y)],'width_mm':.2})
else:raise RuntimeError('Residual routing did not converge')
(P/'reports'/'residual-routing.json').write_text(json.dumps({'method':'conservative-grid; KiCad DRC required','grid_mm':S,'routes':audit,'physical_validation':False},indent=2))

