import json, sys
ICONS = json.load(open(sys.argv[1]))
W, H = 1440, 900
out = []
FG = "#1b1b1b"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,text,size=11,anchor="start",weight="400",fill=FG,halo=True):
    h = f' stroke="#fafafa" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{h}>{esc(text)}</text>')
def group(x,y,w,h,title,stroke,fill,dash=None,icon=None,title_anchor="start"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{d}/>')
    tx = x+10
    if icon:
        out.append(f'<use href="#{icon}" x="{x+8}" y="{y+6}" width="20" height="20"/>'); tx = x+34
    if title_anchor=="end":
        T(x+w-10,y+20,title,size=12,anchor="end",weight="700",fill=stroke,halo=False)
    else:
        T(tx,y+20,title,size=12,weight="700",fill=stroke,halo=False)
def icon(name,cx,cy,size,label,sub=(),fill=None,label_dx=0,label_side="below"):
    ic = ICONS[name]
    f = f' fill="{fill}"' if fill else ""
    out.append(f'<use href="#{name}" x="{cx-size/2}" y="{cy-size/2}" width="{size}" height="{size}"{f}/>')
    if label_side=="below":
        T(cx+label_dx,cy+size/2+14,label,size=11,anchor="middle",weight="700")
        for i,s in enumerate(sub): T(cx+label_dx,cy+size/2+27+i*12,s,size=9.5,anchor="middle",fill="#444")
    else:  # right
        T(cx+size/2+8,cy-2,label,size=11,weight="700")
        for i,s in enumerate(sub): T(cx+size/2+8,cy+11+i*12,s,size=9.5,fill="#444")
def chip(x,y,w,h,title,lines,iconname=None,fill="#fff",iconfill=None):
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="#333" stroke-width="1"/>')
    tx = x+8
    if iconname:
        f = f' fill="{iconfill}"' if iconfill else ""
        out.append(f'<use href="#{iconname}" x="{x+7}" y="{y+7}" width="18" height="18"{f}/>'); tx = x+30
    T(tx,y+20,title,size=11,weight="700",halo=False)
    for i,l in enumerate(lines): T(x+8,y+35+i*12,l,size=9.5,fill="#333",halo=False)
def curve(p0,c0,c1,p1,label=None,lx=None,ly=None,dash=None,color=FG,both=False,num=None,anchor="middle"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    mk = "ah" if color==FG else ("ahg" if color=="#5b6b7b" else "ahr")
    ms = f' marker-start="url(#{mk})"' if both else ""
    out.append(f'<path d="M{p0[0]},{p0[1]} C{c0[0]},{c0[1]} {c1[0]},{c1[1]} {p1[0]},{p1[1]}" fill="none" stroke="{color}" stroke-width="1.4" marker-end="url(#{mk})"{ms}{d}/>')
    if label:
        # default label at bezier t=0.5
        if lx is None:
            lx = (p0[0]+3*c0[0]+3*c1[0]+p1[0])/8; ly = (p0[1]+3*c0[1]+3*c1[1]+p1[1])/8 - 5
        if num is not None:
            out.append(f'<circle cx="{lx-(len(label)*2.9 if anchor=="middle" else 9)}" cy="{ly-4}" r="8" fill="{FG}"/>')
            T(lx-(len(label)*2.9 if anchor=="middle" else 9),ly-0.5,str(num),size=10,anchor="middle",weight="700",fill="#fff",halo=False)
            T(lx+(8 if anchor=="middle" else 4),ly,label,size=10.5,anchor=anchor,fill=color)
        else:
            T(lx,ly,label,size=10.5,anchor=anchor,fill=color)
def person(cx,cy,label,sub=()):
    out.append(f'<circle cx="{cx}" cy="{cy-14}" r="10" fill="none" stroke="{FG}" stroke-width="1.6"/>')
    out.append(f'<path d="M{cx-18},{cy+18} a18,18 0 0 1 36,0" fill="none" stroke="{FG}" stroke-width="1.6"/>')
    T(cx,cy+34,label,size=11,anchor="middle",weight="700")
    for i,s in enumerate(sub): T(cx,cy+47+i*12,s,size=9.5,anchor="middle",fill="#444")

out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="BatchDrop production architecture on AWS: request path from customers through Route 53 to a Dokku-run Rails app on EC2, with RDS, S3, third-party webhooks, and monitoring" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" fill="{FG}">')
out.append('<defs>')
for name,ic in ICONS.items():
    out.append(f'<symbol id="{name}" viewBox="0 0 {ic["w"]} {ic["h"]}">{ic["body"]}</symbol>')
for mid,col in (("ah",FG),("ahg","#5b6b7b"),("ahr","#b5321f")):
    out.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
out.append('</defs>')
out.append(f'<rect width="{W}" height="{H}" fill="#fafafa"/>')

# ---- Boundaries
group(230,46,920,836,"AWS  ·  nowtwollc organization, a Control Tower landing zone with one account per product","#232F3E","#f6f7f9",icon="logos:aws")
group(250,162,880,706,"batchdrop account  ·  Workloads/BatchDrop  ·  us-east-2 (Ohio)","#00A4A6","#eef3f6",dash="6,4")
group(420,322,480,380,"VPC  ·  2 public + 2 isolated subnets, IPv6 on","#8C4FFF","#e9e4f7",icon="logos:aws-vpc",title_anchor="end")
group(438,352,446,160,"Public subnet  ·  one AZ, shared with the database","#7AA116","#ffffff",dash="4,3")
group(438,560,446,122,"Isolated subnets  ·  no route to the internet","#00A4A6","#f3f6f9",dash="4,3")

# ---- Org strip
icon("logos:aws-iam",312,108,40,"IAM Identity Center",("ro · infra · admin profiles","no long-lived keys"),label_side="right")
icon("si:awsorganizations",560,108,34,"Organizations + Control Tower",("management account: domain registration only",),fill="#E7157B",label_side="right")
chip(820,80,318,66,"Company-level infrastructure, applied once",["BatchDropInfra permission set · workload-boundary policy on every role","tfstate bucket · S3 public-access block, EBS encryption, IMDSv2 by default","region-deny guardrail outside the governed regions"])

# ---- Account services
icon("logos:aws-route53",380,250,46,"Route 53 zone batchdrop.io",("serve_from = aws | hetzner, TTL 300","cloned from Namecheap, values unchanged"))
icon("logos:aws-s3",600,244,44,"S3 uploads",("private; Active Storage",),label_side="right")
icon("logos:aws-systems-manager",800,244,44,"SSM Parameter Store",("/batchdrop/DATABASE_URL",),label_side="right")
icon("logos:aws-secrets-manager",330,622,44,"Secrets Manager",("master password, rotated","every 7 days; the app","never uses it"))
icon("logos:aws-route53",400,752,40,"Route 53 health check",("us-east-1 · GET /up every 30 s","3 misses → site-down alarm"))
icon("logos:aws-cloudwatch",1060,760,44,"CloudWatch alarms",("site down · status checks","CPU credits · DB storage"))
icon("logos:aws-sns",850,760,44,"SNS topics",("us-east-2 and us-east-1",))
chip(560,742,250,60,"OpenTofu state and tests",["partial S3 backend in the company's tfstate bucket","tofu test runs against mocked providers, no account"],iconname="si:opentofu",iconfill="#FFDA18")

# ---- Instance and containers
icon("logos:aws-ec2",486,400,46,"EC2 t4g.medium (Graviton) · Dokku",("Elastic IP · IMDSv2, hop limit 2 · encrypted gp3","instance role: uploads, SSM, three _acme TXT names","no state: rebuildable from cloud-init"),label_side="right")
chip(470,440,130,62,"nginx",["Dokku proxy, Let's Encrypt","via DNS-01, 10 MB bodies"],iconname="logos:nginx")
chip(612,440,130,62,"web",["Thruster → Puma, Rails 8","microsite, dashboard, hooks"],iconname="logos:rails")
chip(754,440,124,62,"worker",["Solid Queue: drops, SMS,","receipts, digests"],iconname="logos:docker-icon")
icon("logos:aws-rds",560,626,46,"RDS PostgreSQL 17 · db.t4g.micro",("same AZ · not public · encrypted · 7-day backups","role batchdrop owns the database, created from the box once"),label_side="right")

# ---- People and outside, left
person(118,112,"Operators",("Identity Center SSO","tofu plan/apply · git push · ssh"))
icon("logos:namecheap",118,262,40,"Namecheap",("registrar; nameservers","now point at Route 53"))
icon("si:hetzner",118,372,36,"Hetzner cpx21 (today)",("Dokku, Postgres and uploads on","one box; parallel run until flip"),fill="#D50C2D")
person(118,520,"Customers and creators",("browser and phone",))

# ---- Outside, right
icon("logos:stripe",1290,352,44,"Stripe",("PaymentIntent via Pay gem","signed webhook"))
icon("logos:twilio-icon",1290,450,40,"Twilio + WhatsApp",("one number per store","STOP / START / JOIN consent"))
icon("logos:resend",1290,548,38,"Resend",("SMTP 587, SES-backed","DKIM, SPF, DMARC in the zone"),fill="#000")
person(1290,760,"On call",("email on alarm and on recovery",))

# ---- Flows
# Operators
curve((150,106),(200,106),(250,106),(288,106),"SSO",dash="4,3",color="#5b6b7b")
curve((150,122),(240,160),(250,200),(262,230),"tofu apply, as batchdrop-infra",lx=236,ly=200,dash="4,3",color="#5b6b7b",anchor="start")
curve((150,128),(236,140),(236,404),(462,404),"git push dokku main · ssh",lx=244,ly=392,dash="4,3",color="#5b6b7b",anchor="start")
# DNS cluster
curve((142,262),(250,262),(300,255),(356,252),"nameservers",lx=250,ly=256,dash="4,3",color="#5b6b7b")
curve((356,262),(300,290),(250,340),(140,364),"serve_from = hetzner, today",lx=176,ly=348,dash="4,3",color="#5b6b7b",anchor="start")
curve((392,276),(410,330),(430,360),(464,386),"serve_from = aws → EIP",lx=404,ly=334,anchor="end")
curve((150,506),(250,440),(300,300),(362,272),"DNS lookup",num=1,lx=226,ly=452,anchor="start")
curve((150,520),(260,520),(380,470),(470,470),"HTTPS 443",num=2,lx=320,ly=498)
# nginx writes TXT for Let's Encrypt
curve((500,440),(470,380),(430,330),(402,276),"nginx writes _acme-challenge TXT through the instance role (DNS-01)",lx=520,ly=318,dash="2,3",color="#5b6b7b",anchor="start")
# instance → S3, SSM
curve((486,376),(486,300),(540,262),(578,252),"uploads, credentials from the role over IMDSv2",num=4,lx=560,ly=296,anchor="start")
curve((504,378),(540,316),(720,278),(776,256),"DATABASE_URL, written once at setup",lx=790,ly=300,dash="4,3",color="#5b6b7b",anchor="start")
# web/worker → RDS
curve((677,502),(677,540),(600,560),(572,602),"5432, app security group only",num=3,lx=690,ly=548,anchor="start")
curve((816,502),(816,560),(640,570),(584,606),None)
# Secrets Manager → RDS
curve((354,618),(400,612),(480,612),(536,618),"manages the master password",lx=445,ly=606,dash="4,3",color="#5b6b7b")
# Stripe → web
curve((1266,348),(1100,362),(780,398),(712,440),"signed webhook /webhooks/stripe",num=5,lx=1010,ly=366)
# worker ↔ Twilio
curve((878,464),(1000,462),(1150,452),(1266,450),"SMS out; inbound webhook /webhooks/twilio",num=6,lx=1070,ly=448,both=True)
curve((878,480),(1000,500),(1150,540),(1266,548),"SMTP 587",num=7,lx=1070,ly=530)
# Monitoring
curve((416,730),(430,640),(440,560),(500,504),"GET /up, from outside",lx=448,ly=690,dash="2,3",color="#b5321f",anchor="start")
curve((1038,760),(980,760),(920,760),(876,760),"notify",lx=956,ly=754,color="#b5321f",dash="2,3")
curve((876,772),(980,850),(1200,830),(1266,782),"email, on alarm and on recovery",lx=1090,ly=852,color="#b5321f",dash="2,3")
curve((1060,736),(1060,712),(960,704),(900,700),"instance and database metrics; a failed status check auto-recovers the box",lx=1040,ly=724,color="#b5321f",dash="2,3",anchor="end")

out.append("</svg>")
open(sys.argv[2],"w").write("\n".join(out) + "\n")
print("svg written", sum(len(l) for l in out)//1000, "KB")
