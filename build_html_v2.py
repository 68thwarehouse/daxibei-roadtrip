# -*- coding: utf-8 -*-
# 大西北环线工作台 v2 —— 全量优化版生成器
import math, json

# ---------- 增强行程数据 ----------
# (day,date,route,spots,km,stay,note,alt,temp,meal,road)
itinerary = [
    ("D1","10/01","上海 ✈ 兰州","抵达兰州、取车、中山桥/白塔山",0,"兰州","海拔1520m，黄河之滨",1520,"18/6","火车餐·晚餐兰州牛肉面","无"),
    ("D2","10/02","兰州 → 西宁","塔尔寺、东关清真大寺",240,"西宁","海拔2275m，休整适应",2275,"16/4","手抓羊肉·老酸奶","无"),
    ("D3","10/03","西宁 → 日月山 → 青海湖 → 茶卡盐湖","日月山、青海湖、茶卡盐湖天空之镜",250,"茶卡盐湖","海拔3100m",3100,"11/1","青盐·简餐","西宁出发前加满油"),
    ("D4","10/04","茶卡盐湖 → 德令哈 → 大柴旦","德令哈可鲁克湖、大柴旦翡翠湖",330,"大柴旦","海拔3174m",3174,"13/1","茶卡简餐·大柴旦炕锅","长距离驾驶"),
    ("D5","10/05","大柴旦 → 水上雅丹","U型公路(G315)、水上雅丹",235,"水上雅丹","荒漠路段，备足水",2700,"9/-3","自热饭·营地餐","大柴旦满油！无信号前下离线图"),
    ("D6","10/06","水上雅丹 → 冷湖","火星营地、俄博梁雅丹",120,"冷湖","砂石路、无信号",2800,"9/-4","自热饭·冷湖简餐","砂石路需四驱；勿单车进入"),
    ("D7","10/07","冷湖 → 敦煌","阳关/玉门关可选、敦煌夜市",260,"敦煌","海拔1138m",1138,"20/6","驴肉黄面·夜市","无"),
    ("D8","10/08","敦煌","莫高窟、鸣沙山月牙泉",30,"敦煌","莫高窟需提前预约！",1138,"20/6","杏皮水·胡杨焖饼","无"),
    ("D9","10/09","敦煌 → 酒泉","西汉酒泉胜迹、酒泉公园",380,"酒泉","东风航天城门户",1477,"18/5","糊锅·羊肉粉汤","无"),
    ("D10","10/10","酒泉 → 东风航天城 → 张掖","东风航天城(需预约)、张掖大佛寺",470,"张掖","黄昏看丹霞最佳",1480,"17/4","炒拨拉·搓鱼面","东风航天城需提前审批"),
    ("D11","10/11","张掖 → 七彩丹霞 → 祁连","七彩丹霞、卓尔山·祁连草原",240,"祁连","东方小瑞士",2800,"12/-1","藏餐·牦牛酸奶","垭口可能降雪"),
    ("D12","10/12","祁连 → 门源 → 兰州","门源花海、返兰州",390,"兰州","海拔1520m，黄河之滨",1520,"18/6","兰州牛肉面","无"),
    ("D13","10/13","兰州 → 上海 ✈","还车返程、回上海",0,"—","兰州机场/火车站还车",1520,"18/6","途中餐·返程","无"),
]

budget = [
    ("大交通（往返机票）",5000,3000,"上海⇌兰州，国庆提前订"),
    ("当地交通（租车+油费+过路）",5000,2000,"13天SUV全险，约3000km"),
    ("住宿（12晚）",4200,1200,"兰州×2/西宁/茶卡盐湖/大柴旦/水上雅丹/冷湖/敦煌×2/酒泉/张掖/祁连"),
    ("门票",2500,0,"水上雅丹/茫崖翡翠湖/艾肯泉/莫高窟/鸣沙山/嘉峪关/丹霞/卓尔山等"),
    ("餐饮",3000,0,"兰州牛肉面、敦煌驴肉黄面、张掖搓鱼面等"),
    ("保险",400,0,"意外+高原险+车险"),
    ("购物/特产",1200,0,"枸杞/牦牛肉干/杏干"),
    ("备用金",2000,0,"应急机动（偏远地区用现金）"),
]
BOOKED_CATS = {0:"机票",1:"租车",2:"酒店",3:"门票"}  # 由预订管理回写

bookings = [
    ("往返机票（上海⇌兰州）","航司/携程",3000,"已付","8/31前","—","全员","https://flights.ctrip.com"),
    ("租车（SUV全险）","神州/一嗨",2000,"已付","9/10前","—","主驾","https://www.1hai.cn"),
    ("D1 兰州酒店","携程",320,"待订","9/15前","紧张","全员",""),
    ("D2 西宁酒店","携程",340,"待订","9/15前","","全员",""),
    ("D3 青海湖酒店","美团",360,"待订","9/15前","","全员",""),
    ("D4 大柴旦酒店","携程",380,"待订","9/15前","","全员",""),
    ("D5 水上雅丹酒店","携程",420,"待订","9/15前","紧张","全员",""),
    ("D6 茫崖酒店","携程",360,"待订","9/15前","紧张","全员",""),
    ("D7 冷湖酒店","携程",300,"待订","9/15前","","全员",""),
    ("D8 敦煌酒店","携程",400,"待订","9/15前","","全员",""),
    ("D9 敦煌酒店","携程",400,"待订","9/15前","","全员",""),
    ("D10 嘉峪关酒店","美团",320,"待订","9/15前","","全员",""),
    ("D11 张掖酒店","美团",340,"待订","9/15前","","全员",""),
    ("D12 祁连酒店","携程",300,"待订","9/15前","","全员",""),
    ("莫高窟门票(A类)","官网预约",238,"待订","9/1起约","限流!","全员","https://www.dha.ac.cn"),
    ("水上雅丹门票","现场/线上",120,"待订","9/20前","","全员","https://www.meituan.com"),
    ("茫崖翡翠湖/艾肯泉","现场",150,"待订","9/20前","","全员",""),
    ("火星营地/俄博梁","预约",500,"待订","9/20前","","全员",""),
    ("鸣沙山月牙泉+嘉峪关+丹霞+卓尔山","现场/线上",600,"待订","9/20前","","全员",""),
    ("青海湖/茶卡盐湖门票","现场",220,"待订","9/20前","","全员",""),
]

packing = [
    ("证件票券","身份证","每人必带，登机+住宿","按人","本人"),
    ("证件票券","驾照/行驶证","自驾必备","1套","主驾"),
    ("证件票券","机票/订单截图","离线保存","—","全员"),
    ("证件票券","现金","偏远地区无信号","¥1500","主驾"),
    ("衣物","冲锋衣/羽绒服","10月早晚0-5°C","1件","本人"),
    ("衣物","保暖内衣+抓绒","高原保暖","2套","本人"),
    ("衣物","帽子/围巾/手套","防风保暖","1套","本人"),
    ("衣物","舒适徒步鞋","盐湖/沙漠/雅丹","1双","本人"),
    ("衣物","防风沙面罩","敦煌/雅丹/火星营地","1个","本人"),
    ("数码","手机+充电宝","2万毫安","2个","全员"),
    ("数码","相机+内存卡","风景航拍","1套","摄影"),
    ("数码","车载充电器+逆变器","长途续航","1套","主驾"),
    ("数码","无人机","盐湖/雅丹/丹霞航拍","1台","摄影"),
    ("护肤防晒","高倍防晒(SPF50+)","高原紫外线强","2瓶","全员"),
    ("护肤防晒","墨镜","防雪盲/盐湖反光","1副","全员"),
    ("护肤防晒","润唇膏+保湿","防干裂","各1","全员"),
    ("药品","红景天","提前1周吃防高反","1盒","全员"),
    ("药品","高原安/氧气罐","应急","2罐","主驾"),
    ("药品","感冒/肠胃药+创可贴","常用","1包","全员"),
    ("车载","拖车绳+充气泵","俄博梁/火星营地砂石路","各1","主驾"),
    ("车载","备用油桶/水箱","无人区备用","各1","主驾"),
    ("零食","巧克力/坚果/水","无人区补给","适量","全员"),
    ("其他","颈枕+雨具+垃圾袋","长途舒适","各1","全员"),
]

import json as _json
DEFAULT_BOOKINGS=[{"item":b[0],"ch":b[1],"amt":b[2],"status":b[3],"dl":b[4],"owner":b[6],"note":b[5]} for b in bookings]
DEFAULT_PACKING=[{"cat":p[0],"item":p[1],"note":p[2],"qty":p[3],"owner":p[4],"ok":False} for p in packing]
_DEF_BOOKINGS_JSON=_json.dumps(DEFAULT_BOOKINGS,ensure_ascii=False)
_DEF_PACKING_JSON=_json.dumps(DEFAULT_PACKING,ensure_ascii=False)

food = [
    ("兰州","牛肉面、甜胚子、牛奶鸡蛋醪糟","中山桥夜景、黄河风情线","傍晚","¥15-25/人"),
    ("西宁","手抓羊肉、炕锅羊排、老酸奶","东关清真大寺、莫家街","傍晚","¥60-90/人"),
    ("青海湖","牦牛肉、青稞饼、酥油茶","黑马河日出、湖边经幡","清晨/黄昏","¥70-100/人"),
    ("茶卡","盐雕、青盐","天空之镜镜面倒影","晴天无风","¥30-50/人"),
    ("大柴旦","炕锅、烤串","翡翠湖蒂芙尼蓝、航拍","正午顺光","¥50-80/人"),
    ("水上雅丹","便餐/自热","水上雅丹日落、G315 U型公路","日落","自带"),
    ("茫崖","简单川菜/清真","翡翠湖、艾肯泉(恶魔之眼)航拍","正午","¥40-60/人"),
    ("冷湖","便餐","火星营地、俄博梁雅丹地貌","清晨/黄昏","自带"),
    ("敦煌","驴肉黄面、胡杨焖饼、杏皮水","鸣沙山日落、月牙泉夜景、莫高窟","日落/夜","¥60-100/人"),
    ("嘉峪关","烤肉、搓鱼面","关城城楼剪影","黄昏","¥50-80/人"),
    ("张掖","搓鱼面、炒拨拉","七彩丹霞4号观景台","雨后/黄昏","¥45-70/人"),
    ("祁连","牦牛酸奶、藏餐","卓尔山全景、祁连草原","上午","¥60-90/人"),
]

safety = [
    ("高反预防","兰州1520m→青海湖3200m→大柴旦3174m→茫崖2994m；提前1周服红景天，到后慢走、少洗澡、多喝热水","重要"),
    ("保暖","10月白天10-18°C，早晚0-5°C，垭口可能降雪；必带羽绒+抓绒+帽子手套","重要"),
    ("防晒","高原紫外线极强，墨镜+SPF50+防晒+润唇膏全天；盐湖/沙漠反光更厉害","常规"),
    ("风沙","敦煌、水上雅丹、火星营地风沙大，备防风面罩/口罩，保护相机","重要"),
    ("无人区路况","G315/G215 大柴旦-水上雅丹-茫崖-冷湖段加油站少，提前加满，下载离线地图","重要"),
    ("火星营地/俄博梁","砂石路、无信号，建议四驱SUV，备足水/食物/拖车绳，勿单车进入","关键"),
    ("预约","莫高窟A类票官网提前30天预约，国庆限流极紧张；火星营地需提前预约","重要"),
    ("应急电话","高速救援12328 · 旅游服务12301 · 急救120 · 报警110","关键"),
    ("现金","部分景区/厕所/加油站仅收现金，备¥1000-1500零钱","常规"),
]

# ---------- 地图标记点（腾讯地图 GL JS） ----------
STOPS = [
    {"d":1,"name":"兰州","lat":36.0611,"lng":103.8343,"route":"上海 → 兰州","stay":"兰州","alt":"1520m","km":0},
    {"d":2,"name":"西宁","lat":36.6171,"lng":101.7782,"route":"兰州 → 西宁","stay":"西宁","alt":"2275m","km":240},
    {"d":3,"name":"青海湖","lat":36.8500,"lng":100.2500,"route":"西宁 → 日月山 → 青海湖","stay":"青海湖","alt":"3200m","km":150,"hl":True},
    {"d":4,"name":"大柴旦","lat":37.8533,"lng":95.3667,"route":"青海湖 → 茶卡 → 大柴旦","stay":"大柴旦","alt":"3174m","km":400},
    {"d":5,"name":"水上雅丹","lat":38.1500,"lng":93.4500,"route":"大柴旦 → 水上雅丹","stay":"水上雅丹","alt":"2700m","km":220,"hl":True},
    {"d":6,"name":"茫崖","lat":38.2500,"lng":90.8300,"route":"水上雅丹 → 茫崖","stay":"茫崖","alt":"2994m","km":350,"hl":True},
    {"d":7,"name":"冷湖","lat":38.6300,"lng":93.3200,"route":"茫崖 → 冷湖","stay":"冷湖","alt":"2800m","km":280,"hl":True},
    {"d":8,"name":"敦煌","lat":40.1421,"lng":94.6616,"route":"冷湖 → 敦煌","stay":"敦煌","alt":"1138m","km":260},
    {"d":9,"name":"敦煌","lat":40.1461,"lng":94.6656,"route":"敦煌（莫高窟/鸣沙山）","stay":"敦煌","alt":"1138m","km":30},
    {"d":10,"name":"嘉峪关","lat":39.7731,"lng":98.2905,"route":"敦煌 → 嘉峪关","stay":"嘉峪关","alt":"1600m","km":370},
    {"d":11,"name":"张掖","lat":38.9258,"lng":100.4522,"route":"嘉峪关 → 张掖","stay":"张掖","alt":"1480m","km":230},
    {"d":12,"name":"祁连","lat":38.1833,"lng":100.2500,"route":"张掖 → 祁连","stay":"祁连","alt":"2800m","km":200},
    {"d":13,"name":"西宁","lat":36.6171,"lng":101.7782,"route":"祁连 → 西宁 → 上海","stay":"—","alt":"2275m","km":290},
]

# ---------- SVG: 海拔+温度曲线 ----------
def build_alt_svg():
    alts=[d[7] for d in itinerary]; temps=[d[8] for d in itinerary]
    n=len(alts); W,H=620,170; pl,pr,pt,pb=34,14,14,24
    iw=W-pl-pr; ih=H-pt-pb
    amin,amax=min(alts),max(alts)
    def X(i): return pl+i/(n-1)*iw
    def Y(a): return pt+ih-(a-amin)/(amax-amin)*ih
    parts=[]
    # grid
    for g in range(4):
        yy=pt+ih*g/3; parts.append(f'<line x1="{pl}" y1="{yy:.1f}" x2="{W-pr}" y2="{yy:.1f}" stroke="#eef2f6"/>')
    # area+line
    pts=[(X(i),Y(a)) for i,a in enumerate(alts)]
    line=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    parts.append(f'<polyline points="{line}" fill="none" stroke="#4a6d8c" stroke-width="2.5"/>')
    for i,(x,y) in enumerate(pts):
        big = alts[i]==amax
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 if big else 3}" fill="{ "#c97b5a" if big else "#4a6d8c"}"/>')
        if big: parts.append(f'<text x="{x:.1f}" y="{y-9:.1f}" text-anchor="middle" font-size="11" fill="#c97b5a">峰值 {alts[i]}m</text>')
    # x labels
    for i,d in enumerate(itinerary):
        if i%2==0 or i==n-1:
            parts.append(f'<text x="{X(i):.1f}" y="{H-8}" text-anchor="middle" font-size="10" fill="#7d8a99">{d[0]}</text>')
    # y labels
    parts.append(f'<text x="{pl-4}" y="{pt+4}" text-anchor="end" font-size="10" fill="#7d8a99">{amax}</text>')
    parts.append(f'<text x="{pl-4}" y="{pt+ih}" text-anchor="end" font-size="10" fill="#7d8a99">{amin}</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:680px;display:block;margin:0 auto">{ "".join(parts) }</svg>'

# ---------- SVG: 路线地图 ----------
def build_route_svg():
    nodes={"兰州":(560,250),"西宁":(520,220),"青海湖":(470,210),"大柴旦":(385,190),
           "水上雅丹":(320,212),"茫崖":(175,250),"冷湖":(300,178),"敦煌":(360,232),
           "嘉峪关":(440,208),"张掖":(498,180),"祁连":(500,138)}
    order=["兰州","西宁","青海湖","大柴旦","水上雅丹","茫崖","冷湖","敦煌","嘉峪关","张掖","祁连"]
    W,H=620,300
    parts=[]
    # path
    coords=[nodes[c] for c in order]
    path=" ".join(f"{x},{y}" for x,y in coords)
    parts.append(f'<polyline points="{path}" fill="none" stroke="#cdd8e2" stroke-width="2.5" stroke-dasharray="5 4"/>')
    # nodes
    for c,(x,y) in nodes.items():
        fill = "#c97b5a" if c in ("茫崖","冷湖","水上雅丹") else "#4a6d8c"
        parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{fill}"/>')
        dy = -12 if y>200 else 14
        parts.append(f'<text x="{x}" y="{y+dy}" text-anchor="middle" font-size="11" fill="#2b3a4a">{c}</text>')
    # start/end markers
    parts.append(f'<text x="{nodes["兰州"][0]}" y="{nodes["兰州"][1]+22}" text-anchor="middle" font-size="10" fill="#4a6d8c">起</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:680px;display:block;margin:0 auto">{ "".join(parts) }</svg>'

ALT_SVG=build_alt_svg()
ROUTE_SVG=build_route_svg()

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# ---------- 行程时间轴（由 JS 从地点库+计划渲染，见 JS2） ----------
# 注：卡片在浏览器端根据 LOC_DB / state.plan 动态生成，便于结构化编辑。

# ---------- 预算表 ----------
budget_html=""
for i,(cat,plan,paid,note) in enumerate(budget):
    if i in BOOKED_CATS:
        paid_cell=f'<td class="bd-wait" id="bd-paid-{i}">—</td>'
    else:
        paid_cell=f'<td><input class="num" id="bd-paid-{i}" type="number" value="{paid}" oninput="recompute()"></td>'
    budget_html+=f"""
    <tr>
      <td>{esc(cat)}</td>
      <td><input class="num" id="bd-plan-{i}" type="number" value="{plan}" oninput="recompute()"></td>
      {paid_cell}
      <td class="bd-wait" id="bd-wait-{i}">—</td>
      <td class="note">{esc(note)}</td>
    </tr>"""

# ---------- 预订 ----------
# ---------- 美食 ----------
food_html=""
for city,f,ph,t,price in food:
    food_html+=f"""
    <div class="food-card">
      <div class="food-city">{esc(city)}</div>
      <div class="food-row"><span class="lbl">🍜</span>{esc(f)}</div>
      <div class="food-row"><span class="lbl">📷</span>{esc(ph)}</div>
      <div class="food-row"><span class="lbl">⏰</span>{esc(t)} · <b>{esc(price)}</b></div>
    </div>"""

# ---------- 安全 ----------
lvl_cls={"关键":"lv-key","重要":"lv-imp","常规":"lv-nor"}
safety_html=""
for theme,point,lvl in safety:
    safety_html+=f"""
    <div class="safe-card">
      <div class="safe-head"><span class="safe-theme">{esc(theme)}</span><span class="badge {lvl_cls[lvl]}">{lvl}</span></div>
      <div class="safe-point">{esc(point)}</div>
    </div>"""

# ---------- 模块导航 ----------
modules=[("行程总表","itinerary","live","已排","#4a6d8c"),("预算追踪","budget","auto","可填","#c97b5a"),
         ("预订管理","booking","live","进行中","#6b9b8a"),("行李清单","packing","live","未开始","#8a7ca8"),
         ("美食&拍照","food","—","参考","#b56b6b"),
         ("高原&安全","safety","—","参考","#5a8f7b")]
nav_html=""
for name,anchor,comp,status,color in modules:
    nav_html+=f"""
    <a class="mod-card" href="#sec-{anchor}" style="--mc:{color}">
      <div class="mod-name">{name}</div>
      <div class="mod-bar"><div class="mod-fill" id="modfill-{anchor}" style="background:{color}"></div></div>
      <div class="mod-meta"><span id="modpct-{anchor}">{comp}</span><span class="mod-status">{status}</span></div>
    </a>"""

NIT=len(itinerary)

HTML=f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大西北环线 · 13日自驾工作台 v2</title>
<style>
:root{{--blue:#4a6d8c;--orange:#c97b5a;--green:#6b9b8a;--purple:#8a7ca8;
  --ink:#2b3a4a;--muted:#7d8a99;--line:#e6edf3;--card:#ffffff;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;color:var(--ink);line-height:1.6;
  background:linear-gradient(135deg,#eef3f7 0%,#f3f6f4 45%,#fbf4ec 100%);background-attachment:fixed;padding-bottom:60px}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 18px}}
.hero{{background:linear-gradient(120deg,#4a6d8c,#5b86a0 50%,#6b9b8a);border-radius:0 0 28px 28px;color:#fff;
  padding:28px 24px 24px;box-shadow:0 10px 30px rgba(74,109,140,.22)}}
.hero h1{{font-size:24px;letter-spacing:1px}}
.hero .sub{{opacity:.92;font-size:13.5px;margin-top:6px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px;align-items:center}}
.kpi{{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);border-radius:16px;padding:12px;text-align:center}}
.kpi .v{{font-size:24px;font-weight:800;line-height:1.1}}
.kpi .l{{font-size:12px;opacity:.9;margin-top:4px}}
.donut-kpi{{display:flex;align-items:center;gap:10px;justify-content:center}}
.donut-kpi svg{{flex:0 0 auto}}
.shared-banner{{max-width:1080px;margin:12px auto 0;padding:8px 14px;border-radius:10px;font-size:12.5px;font-weight:600;text-align:center}}
.shared-banner.on{{background:#e8f6ee;color:#1f8a4c;border:1px solid #bfe6cd}}
.shared-banner.off{{background:#fff6e8;color:#9a6b1f;border:1px solid #f0d9a8}}
.toolbar{{display:flex;gap:10px;justify-content:flex-end;margin:14px 0}}
.btn{{background:#fff;border:1px solid var(--line);border-radius:10px;padding:7px 14px;font-size:12.5px;cursor:pointer;color:var(--ink);font-family:inherit}}
.btn:hover{{border-color:var(--blue);color:var(--blue)}}
.nav{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0}}
.mod-card{{display:block;text-decoration:none;color:var(--ink);background:var(--card);border-radius:14px;padding:12px;
  border-top:3px solid var(--mc);box-shadow:0 4px 14px rgba(40,60,80,.07);transition:.18s}}
.mod-card:hover{{transform:translateY(-3px);box-shadow:0 8px 20px rgba(40,60,80,.13)}}
.mod-name{{font-weight:700;font-size:14px}}
.mod-bar{{height:7px;background:#eef2f6;border-radius:5px;margin:8px 0 6px;overflow:hidden}}
.mod-fill{{height:100%;width:0;border-radius:5px;transition:width .5s}}
.mod-meta{{display:flex;justify-content:space-between;align-items:center;font-size:11.5px}}
.mod-meta span:first-child{{font-weight:700;color:var(--mc)}}
.mod-status{{background:#f0f3f6;color:var(--muted);border-radius:20px;padding:1px 8px}}
.sec{{background:var(--card);border-radius:18px;padding:20px;margin:18px 0;box-shadow:0 6px 22px rgba(40,60,80,.08)}}
.sec-h{{display:flex;align-items:center;gap:9px;font-size:18px;font-weight:800;margin-bottom:14px;flex-wrap:wrap}}
.sec-h .ic{{font-size:21px}}
.sec-h .hint{{font-size:12px;font-weight:500;color:var(--muted);margin-left:auto}}
.prog{{height:9px;background:#eef2f6;border-radius:6px;overflow:hidden;margin-bottom:14px}}
.prog>div{{height:100%;border-radius:6px;transition:width .5s}}
.map-box{{background:#f8fbfd;border:1px solid var(--line);border-radius:14px;padding:14px;margin-bottom:14px;text-align:center}}
.chart-box{{background:#f8fbfd;border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:14px}}
.chart-cap{{font-size:12px;color:var(--muted);text-align:center;margin-top:4px}}
.tl-item{{display:flex;gap:14px;position:relative}}
.tl-item:not(:last-child)::before{{content:"";position:absolute;left:19px;top:40px;bottom:0;width:2px;background:linear-gradient(var(--blue),var(--green))}}
.tl-dot{{flex:0 0 40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--blue),var(--green));color:#fff;
  font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;z-index:2;box-shadow:0 3px 10px rgba(74,109,140,.3)}}
.tl-card{{flex:1;background:#f8fbfd;border:1px solid var(--line);border-radius:13px;padding:11px 14px;margin-bottom:14px}}
.tl-head{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-weight:700}}
.tl-date{{background:var(--blue);color:#fff;border-radius:7px;padding:1px 8px;font-size:12.5px}}
.tl-route{{font-size:14.5px}}
.tl-km{{margin-left:auto;color:var(--orange);font-size:12.5px;font-weight:700}}
.day-done{{font-size:12px;color:var(--muted);font-weight:500;display:flex;align-items:center;gap:4px;margin-left:8px}}
.tl-spots{{color:var(--ink);font-size:13.5px;margin:5px 0}}
.tl-foot{{display:flex;flex-wrap:wrap;gap:6px;font-size:12px}}
.tag-stay{{background:#eaf4ee;color:var(--green);border-radius:20px;padding:1px 9px}}
.tag-alt,.tag-temp,.tag-meal{{background:#eef2f6;color:#5a6b7b;border-radius:20px;padding:1px 9px}}
.tag-note{{background:#fdf0e6;color:var(--orange);border-radius:20px;padding:1px 9px}}
.tag-warn{{background:#fdecea;color:#c0392b;border-radius:20px;padding:1px 9px;font-weight:600}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:left;color:var(--muted);font-weight:600;font-size:12px;border-bottom:2px solid var(--line);padding:8px 6px}}
td{{padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}}
tr:hover td{{background:#fafcfe}}
.muted{{color:var(--muted)}}.note{{color:var(--muted);font-size:12px}}
.num{{width:78px;padding:5px 7px;border:1px solid var(--line);border-radius:8px;font-size:13px;text-align:right;font-family:inherit}}
.num:focus{{outline:none;border-color:var(--blue);box-shadow:0 0 0 2px rgba(74,109,140,.12)}}
.pin{{width:100%;padding:5px 7px;border:1px solid var(--line);border-radius:8px;font-size:12.5px;font-family:inherit;min-width:90px}}
.pin:focus{{outline:none;border-color:var(--blue)}}
.bd-wait{{font-weight:700;color:var(--orange)}}
.st{{padding:5px 8px;border-radius:8px;border:1px solid var(--line);font-size:12.5px;font-family:inherit;cursor:pointer;font-weight:600;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6'><path d='M0 0l5 6 5-6z' fill='%23666'/></svg>");background-repeat:no-repeat;background-position:right 6px center;padding-right:20px}}
.st.s-paid{{background-color:#e8f6ee;color:#1f8a4c;border-color:#9fd6b3}}
.st.s-booked{{background-color:#eaf1fb;color:#3461b0;border-color:#a9c4ec}}
.st.s-todo{{background-color:#f3f4f6;color:#7d8a99;border-color:#d7dee6}}
.bk-in{{width:100%;min-width:74px;padding:4px 6px;border:1px solid var(--line);border-radius:7px;font-size:12.5px;font-family:inherit;background:#fff}}
.bk-amt{{width:74px;padding:4px 6px;border:1px solid var(--line);border-radius:7px;font-size:13px;text-align:right;font-family:inherit;background:#fff}}
.bk-in:focus,.bk-amt:focus{{outline:none;border-color:var(--blue);box-shadow:0 0 0 2px rgba(74,109,140,.12)}}
.ck{{width:18px;height:18px;cursor:pointer;accent-color:var(--green)}}
.cat-cell{{background:#f5f8fb;font-weight:600;color:var(--blue)}}
.add-btn{{border:1px solid var(--blue);background:#eef4f8;color:var(--blue);border-radius:8px;padding:3px 10px;font-size:12px;font-family:inherit;cursor:pointer;margin-left:8px}}
.add-btn:hover{{background:#e0ebf2}}
.bk-item-cell{{position:relative;padding-right:24px!important}}
.row-del{{position:absolute;right:4px;top:50%;transform:translateY(-50%);border:none;background:#f3e3e3;color:#c0392b;border-radius:6px;width:18px;height:18px;line-height:16px;font-size:11px;cursor:pointer;padding:0}}
.row-del:hover{{background:#e8cccc}}
.flag{{background:#fdecea;color:#c0392b;font-size:11px;border-radius:6px;padding:1px 6px}}
.lk{{text-decoration:none}}
tfoot td{{font-weight:800;border-top:2px solid var(--line);border-bottom:none}}
.food-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.food-card{{background:#f8fbfd;border:1px solid var(--line);border-radius:13px;padding:12px}}
.food-city{{font-weight:800;color:var(--orange);font-size:15px;margin-bottom:6px}}
.food-row{{font-size:12.5px;margin:3px 0;display:flex;gap:6px}}
.food-row .lbl{{flex:0 0 16px}}
.safe-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.safe-card{{background:#f8fbfd;border:1px solid var(--line);border-radius:13px;padding:13px}}
.safe-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}}
.safe-theme{{font-weight:800;font-size:14px}}
.safe-point{{font-size:12.5px;color:#51606f}}
.badge{{font-size:11px;border-radius:20px;padding:2px 9px;font-weight:600}}
.lv-key{{background:#fdecea;color:#c0392b}}.lv-imp{{background:#fdf0e6;color:#d35400}}.lv-nor{{background:#eef2f6;color:#5a6b7b}}
.p-high{{background:#fdecea;color:#c0392b}}.p-mid{{background:#fdf0e6;color:#d35400}}
.ft{{text-align:center;color:var(--muted);font-size:12px;margin-top:24px}}
@media(max-width:760px){{.kpis{{grid-template-columns:repeat(2,1fr)}}.nav{{grid-template-columns:repeat(2,1fr)}}
  .food-grid,.safe-grid{{grid-template-columns:1fr}}.hero h1{{font-size:21px}}}}
@media print{{.nav,.toolbar{{display:none}}body{{background:#fff;padding:0}}
  .sec{{box-shadow:none;page-break-inside:avoid;margin:10px 0}}.hero{{box-shadow:none;border-radius:0}}}}
</style>
<style>
.tmap-wrap{{position:relative;border-radius:14px;overflow:hidden}}
#tmap{{width:100%;height:520px;background:#eef3f7}}
.map-legend{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;font-size:12.5px;color:#51606f;margin-top:10px}}
.map-legend .dot{{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:-1px}}
.map-legend .ln{{display:inline-block;width:24px;height:0;border-top:3px solid #4a6d8c;margin-right:6px;vertical-align:3px}}
.map-tip{{font-size:12px;color:#9aa7b4;margin-top:8px;line-height:1.5}}
.it-date{{width:60px;font:inherit;font-weight:700;color:#2b3a4a;border:1px solid #d7dee6;border-radius:7px;padding:3px 6px;background:#fff;font-size:13px}}
.it-date[readonly]{{background:#eef2f6;color:#5a6b7b;cursor:default;border-style:dashed}}
.it-loc{{font:inherit;font-weight:700;color:#2b3a4a;border:1px solid #d7dee6;border-radius:7px;padding:3px 6px;background:#fff;font-size:13px;max-width:170px}}
.tl-route-line{{margin:3px 0 5px;color:#7d8a99;font-size:13px}}
.tl-locs{{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin:6px 0 4px}}
.loc-cell{{display:inline-flex;align-items:center;gap:3px}}
.loc-role{{font-size:10.5px;color:#8a98a6;background:#eef2f6;border-radius:5px;padding:1px 5px;margin-right:2px;white-space:nowrap}}
.arr{{color:#9aa7b4;margin:0 1px}}
.it-addmid{{font:inherit;font-size:12px;color:#2b6d4f;background:#eaf6ef;border:1px solid #bfe3cd;border-radius:7px;padding:2px 8px;cursor:pointer;margin-left:6px;white-space:nowrap}}
.it-addmid:hover{{background:#dcefe2}}
.it-delmid{{font:inherit;font-size:12px;line-height:1;color:#c0392b;background:#fdecea;border:1px solid #f3c4bd;border-radius:50%;width:18px;height:18px;cursor:pointer;padding:0;margin-left:2px}}
.it-delmid:hover{{background:#f9d6d2}}
.tag-fly{{display:inline-block;margin-left:8px;font-size:11px;color:#2b6cb0;background:#e8f1fb;border-radius:6px;padding:1px 7px;vertical-align:1px}}
.it-ctrl{{margin-left:auto;display:flex;gap:8px}}
.leaflet-div-icon.rw-pin{{background:transparent;border:none}}
.tl-item.active .tl-card{{outline:2px solid #c97b5a;box-shadow:0 0 0 3px rgba(201,123,90,.18)}}
.dl-warn{{display:none;background:#fdecea;color:#c0392b;border-radius:10px;padding:9px 14px;font-size:12.5px;margin-bottom:12px}}
.dl-over{{color:#c0392b;font-weight:700}}
.dl-near{{color:#d35400;font-weight:700}}
.route-static{{display:none}}
@media print{{#tmap{{display:none}}.route-static{{display:block!important}}}}
</style>
<script type="text/javascript">
  window._TMapSecurityConfig = {{
    serviceHost: 'http://127.0.0.1:__WB_HTTP_PORT__/_TMapService/_wbt/__WB_TMAP_SECRET__',
  }};
</script>
<script src="https://map.qq.com/api/gljs?v=1.exp"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css" crossorigin="" />
<script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
</head>
<body>
<header class="hero"><div class="wrap">
  <h1>🏔️ 大西北环线 · 13日自驾之旅 v2</h1>
  <div class="sub">13天12晚 · 上海往返·兰州进出 · 国庆自驾 · 出发日 2026-10-01</div>
  <div class="kpis">
    <div class="kpi"><div class="v" id="k-countdown">—</div><div class="l">距出发</div></div>
    <div class="kpi"><div class="v" id="k-budget">—</div><div class="l">总预算</div></div>
    <div class="kpi"><div class="v" id="k-paid">—</div><div class="l">已付(预订回写)</div></div>
    <div class="kpi donut-kpi">
      <svg width="62" height="62" viewBox="0 0 62 62">
        <circle cx="31" cy="31" r="26" fill="none" stroke="#eef2f6" stroke-width="7"/>
        <circle id="donut" cx="31" cy="31" r="26" fill="none" stroke="#6b9b8a" stroke-width="7" stroke-linecap="round" transform="rotate(-90 31 31)" stroke-dasharray="163.4" stroke-dashoffset="163.4"/>
        <text id="donut-txt" x="31" y="35" text-anchor="middle" font-size="13" font-weight="800" fill="#2b3a4a">0%</text>
      </svg>
      <div style="text-align:left"><div style="font-size:13px;font-weight:700">整体完成</div><div style="font-size:11px;opacity:.85">实时</div></div>
    </div>
  </div>
</div></header>

<div id="shared-banner" class="shared-banner" style="display:none"></div>

<div class="wrap">
  <div class="toolbar">
    <button class="btn" onclick="window.print()">🖨 打印行程单</button>
    <button class="btn" onclick="exportJSON()">⬇ 导出备份</button>
    <button class="btn" onclick="document.getElementById('importFile').click()">⬆ 导入备份</button>
    <input id="importFile" type="file" accept="application/json,.json" style="display:none" onchange="importJSON(this)">
    <button class="btn" onclick="resetAll()">↺ 重置勾选</button>
  </div>
  <nav class="nav">{nav_html}</nav>

  <section class="sec" id="sec-itinerary">
    <div class="sec-h"><span class="ic">🗺️</span>行程总表
      <span class="it-ctrl">
        <button class="btn" onclick="addDay()">＋ 加一天</button>
        <button class="btn" onclick="delDay()">－ 删一天</button>
      </span>
      <span class="hint">改「地点」即自动算景点·距离·海拔·油费（日期已固定 10/01–10/13）</span></div>
    <div class="map-box">
  <div class="tmap-wrap">
    <div id="tmap"></div>
    <button class="btn" style="position:absolute;top:12px;right:12px;z-index:5;box-shadow:0 2px 8px rgba(0,0,0,.12)" onclick="fitRoute()">⤢ 全览路线</button>
  </div>
  <div class="map-legend">
    <span><span class="ln"></span>自驾路线（环线）</span>
    <span><span class="dot" style="background:#c97b5a"></span>无人区住宿点</span>
    <span><span class="dot" style="background:#4a6d8c"></span>城市/途经点</span>
    <span class="muted">点击地图标记或下方行程卡片可联动定位</span>
  </div>
  <div class="map-tip">交互地图可拖拽 / 缩放，点击地图标记或下方行程卡片可联动定位。分享给他人的链接同样可交互。</div>
  <div id="route-static" class="route-static">{ROUTE_SVG}<div class="chart-cap">路线示意图（打印/离线版）</div></div>
</div>
    <div class="chart-box">{ALT_SVG}<div class="chart-cap">每日海拔曲线（红点=最高点青海湖 3200m）· 温度见每日卡片</div></div>
    <div class="prog"><div id="it-prog" style="background:linear-gradient(90deg,var(--blue),var(--green))"></div></div>
    <div id="it-list"></div>
    <div style="margin-top:8px;padding:12px 14px;background:#f8fbfd;border:1px dashed var(--line);border-radius:12px;font-size:12.5px;color:#51606f">
      💡 G315/G215 茫崖-冷湖段多为荒漠无人区，提前加满油、下载离线地图；火星营地/俄博梁为砂石路，建议四驱SUV且备足水/食物。
    </div>
  </section>

  <section class="sec" id="sec-budget">
    <div class="sec-h"><span class="ic">💰</span>预算追踪<span class="hint">按 <input id="pax" class="num" style="width:48px" value="2" oninput="recompute()"> 人估算 · 已付由预订回写</span></div>
    <table>
      <thead><tr><th>类别</th><th>预算</th><th>已付</th><th>待付</th><th>说明</th></tr></thead>
      <tbody>{budget_html}</tbody>
      <tfoot><tr><td>合计</td><td id="bd-total">—</td><td id="bd-paidtotal">—</td><td id="bd-waittotal">—</td><td></td></tr></tfoot>
    </table>
    <div style="display:flex;gap:18px;margin-top:12px;font-size:13px;flex-wrap:wrap">
      <span>已付占比 <b id="bd-paidpct" style="color:var(--green)">—</b></span>
      <span>待付占比 <b id="bd-waitpct" style="color:var(--orange)">—</b></span>
      <span>预订已付回写 <b id="bk-paid-sum" style="color:var(--blue)">—</b></span>
    </div>
  </section>

  <section class="sec" id="sec-booking">
    <div class="sec-h"><span class="ic">📌</span>预订管理<span class="hint">酒店随行程住宿自动对齐 · 状态可下拉 · 自由增减</span>
      <button class="add-btn" type="button" onclick="addBooking()">＋ 新增项目</button></div>
    <div style="margin-bottom:10px"><label style="font-size:13px">按人查看：
      <select id="personFilter" onchange="applyFilter()" style="padding:5px 8px;border-radius:8px;border:1px solid var(--line);font-family:inherit">
        <option value="all">全部</option><option value="主驾">主驾</option><option value="摄影">摄影</option><option value="全员">全员</option>
      </select></label></div>
    <div class="prog"><div id="bk-prog" style="background:linear-gradient(90deg,var(--green),var(--blue))"></div></div>
    <table>
      <thead><tr><th>项目</th><th>渠道</th><th>金额</th><th>状态</th><th>截止</th><th>负责人</th><th>备注</th></tr></thead>
      <tbody id="bk-list"></tbody>
    </table>
  </section>

  <section class="sec" id="sec-packing">
    <div class="sec-h"><span class="ic">🎒</span>行李清单<span class="hint">勾选计入完成度 · 自由增减</span>
      <button class="add-btn" type="button" onclick="addPacking()">＋ 新增物品</button></div>
    <div class="prog"><div id="pk-prog" style="background:linear-gradient(90deg,var(--purple),#b56fb0)"></div></div>
    <table>
      <thead><tr><th>分类</th><th>物品</th><th>数量</th><th>负责人</th><th style="text-align:center">已确认</th></tr></thead>
      <tbody id="pk-list"></tbody>
    </table>
  </section>

  <section class="sec" id="sec-food">
    <div class="sec-h"><span class="ic">🍜</span>美食 & 拍照地图</div>
    <div class="food-grid">{food_html}</div>
  </section>

  <section class="sec" id="sec-safety">
    <div class="sec-h"><span class="ic">⛑️</span>高原 & 安全贴士</div>
    <div class="safe-grid">{safety_html}</div>
  </section>

  <div class="ft">大西北环线工作台 v2 · 数据本地缓存 + 云端共享（多人实时同步）· 出发日 2026-10-01</div>
</div>

<script>
const DEPART=new Date(2026,9,1);
const KEY='dqx_workbench_v2';
const BOOKED_CATS={{0:'机票',1:'租车',2:'酒店',3:'门票'}};
const PER=[1,0,0,1,1,1,0,0]; // 人均项：机票/门票/餐饮/保险随人数缩放，其余固定
let state=JSON.parse(localStorage.getItem(KEY)||'{{}}');

function save(){{localStorage.setItem(KEY,JSON.stringify(state)); if(window.__sharedReady)window.SharedSync.push(state);}}
function setMod(a,p){{const f=document.getElementById('modfill-'+a),p2=document.getElementById('modpct-'+a);
  if(f)f.style.width=p+'%'; if(p2&&p!=='auto')p2.textContent=p+'%';}}

function classifyBooking(item){{
  if('机票'===item||item.indexOf('机票')>=0)return 0;
  if(item.indexOf('租车')>=0)return 1;
  if(item.indexOf('酒店')>=0)return 2;
  if(item.indexOf('门票')>=0||item.indexOf('莫高窟')>=0||item.indexOf('雅丹')>=0||item.indexOf('翡翠湖')>=0||
     item.indexOf('艾肯泉')>=0||item.indexOf('火星')>=0||item.indexOf('丹霞')>=0||item.indexOf('卓尔')>=0||
     item.indexOf('茶卡')>=0||item.indexOf('盐湖')>=0)return 3;
  return -1;
}}

function recompute(){{
  const pax=Math.max(1,+document.getElementById('pax').value||2);
  // 预算（人均项随人数缩放：仅在人数变化时按比例缩放，尊重手动修改）
  if(typeof state.pax!=='number')state.pax=pax;
  if(state.pax!==pax){{const ratio=pax/state.pax;
    for(let i=0;i<{len(budget)};i++){{if(PER[i]){{const el=document.getElementById('bd-plan-'+i);
      el.value=Math.round((+el.value||0)*ratio);}}}} state.pax=pax;}}
  // 预订（先于预算，计算已付回写 + 完成度）
  let done=0; const paidMap={{0:0,1:0,2:0,3:0}};
  const bkRows=document.querySelectorAll('#bk-list tr');
  state.bookings=[];
  bkRows.forEach(function(tr){{ const b=readBookingRow(tr); state.bookings.push(b);
    if(b.status==='已付'){{const c=classifyBooking(b.item); if(c>=0)paidMap[c]+=+b.amt||0;}}
    if(b.status==='已订'||b.status==='已付')done++; }});
  const bkp=Math.round(done/Math.max(1,bkRows.length)*100);
  document.getElementById('bk-prog').style.width=bkp+'%'; setMod('booking',bkp);
  // 预算
  let total=0,paid=0;
  for(let i=0;i<{len(budget)};i++){{
    let b=+document.getElementById('bd-plan-'+i).value||0;
    document.getElementById('bd-plan-'+i).value=b; total+=b;
    let p;
    if(i in BOOKED_CATS){{p=paidMap[i];document.getElementById('bd-paid-'+i).textContent='¥'+p;}}
    else{{p=+document.getElementById('bd-paid-'+i).value||0;}}
    paid+=p;
    document.getElementById('bd-wait-'+i).textContent='¥'+(b-p);
  }}
  document.getElementById('bd-total').textContent='¥'+total.toLocaleString();
  document.getElementById('bd-paidtotal').textContent='¥'+paid.toLocaleString();
  document.getElementById('bd-waittotal').textContent='¥'+(total-paid).toLocaleString();
  const ppct=total>0?Math.round(paid/total*100):0;
  document.getElementById('bd-paidpct').textContent=ppct+'%';
  document.getElementById('bd-waitpct').textContent=(100-ppct)+'%';
  document.getElementById('bk-paid-sum').textContent='¥'+paid.toLocaleString();
  document.getElementById('k-budget').textContent='¥'+total.toLocaleString();
  document.getElementById('k-paid').textContent='¥'+paid.toLocaleString();
  setMod('budget',ppct);

  // 行程每日
  let it=0;
  for(let i=0;i<{{DAY_COUNT}};i++){{const c=document.getElementById('day-'+i);if(state['day-'+i])c.checked=true;
    if(c.checked)it++; state['day-'+i]=c.checked;}}
  const itp=Math.round(it/{{DAY_COUNT}}*100);
  document.getElementById('it-prog').style.width=itp+'%'; setMod('itinerary',itp);

  // 行李
  let pk=0; const pkRows=document.querySelectorAll('#pk-list tr'); state.packing=[];
  pkRows.forEach(function(tr){{ const p=readPackingRow(tr); state.packing.push(p); if(p.ok)pk++; }});
  const pkp=Math.round(pk/Math.max(1,pkRows.length)*100);
  document.getElementById('pk-prog').style.width=pkp+'%'; setMod('packing',pkp);

  // 整体
  const overall=Math.round((bkp+itp+pkp)/3);
  const donut=document.getElementById('donut');
  donut.style.strokeDashoffset=163.4*(1-overall/100);
  document.getElementById('donut-txt').textContent=overall+'%';

  save();
}}

function applyFilter(){{
  const v=document.getElementById('personFilter').value;
  document.querySelectorAll('#sec-booking tbody tr,#sec-packing tbody tr').forEach(tr=>{{
    const o=tr.getAttribute('data-owner')||'';
    const show = v==='all' || o.indexOf(v)>=0;
    tr.style.display=show?'':'none';
  }});
}}

function resetAll(){{state={{}};localStorage.removeItem(KEY);location.reload();}}

(function(){{const now=new Date();const days=Math.ceil((DEPART-now)/86400000);
  document.getElementById('k-countdown').innerHTML=(days>0?days:'0')+'<small> 天</small>';}})();


</script>
<script>
__JS2__
</script>
</body>
</html>"""

# ---------- 第二段脚本：地图初始化 + 截止日预警 + 备份导入导出 ----------
JS2 = r"""/* ===== 行程总表 · 可交互地图（腾讯地图 GL JS，合规代理，无需密钥） ===== */
/* ===== 地点数据库：改「日期 / 地点」即自动推导景点·距离·海拔·油费 ===== */
const LOC_DB={
 '上海':{name:'上海',lat:31.2304,lng:121.4737,alt:4,temp:'25/18',spots:'浦东机场 · 外滩',meal:'本帮菜·小笼',note:'出发地',hl:false},
 '兰州':{name:'兰州',lat:36.0611,lng:103.8343,alt:1520,temp:'18/6',spots:'中山桥 · 白塔山 · 甘肃省博',meal:'兰州牛肉面·牛奶鸡蛋醪糟',note:'黄河之滨',hl:false},
 '西宁':{name:'西宁',lat:36.6171,lng:101.7782,alt:2275,temp:'16/4',spots:'塔尔寺 · 东关清真大寺',meal:'手抓羊肉·老酸奶',note:'休整适应',hl:false},
 '青海湖':{name:'青海湖',lat:36.8500,lng:100.2500,alt:3200,temp:'12/0',spots:'二郎剑 · 黑马河 · 环湖',meal:'牦牛肉·青稞饼',note:'勿跑跳少洗澡',hl:true},
 '茶卡盐湖':{name:'茶卡盐湖',lat:36.7833,lng:99.0833,alt:3100,temp:'11/1',spots:'天空之镜 · 盐雕',meal:'青盐·简餐',note:'晴天无风最佳',hl:false},
 '大柴旦':{name:'大柴旦',lat:37.8533,lng:95.3667,alt:3174,temp:'13/1',spots:'大柴旦翡翠湖 · 雪山温泉',meal:'炕锅·烤串',note:'备足水',hl:false},
 '德令哈':{name:'德令哈',lat:37.3735,lng:97.3789,alt:2980,temp:'11/-1',spots:'可鲁克湖 · 柏树山',meal:'炕锅',note:'',hl:false},
 '水上雅丹':{name:'水上雅丹',lat:38.1500,lng:93.4500,alt:2700,temp:'9/-3',spots:'乌素特水上雅丹 · G315 U型公路',meal:'自热饭·营地餐',note:'荒漠备水',hl:true},
 '茫崖':{name:'茫崖',lat:38.2500,lng:90.8300,alt:2994,temp:'8/-4',spots:'艾肯泉(恶魔之眼) · 茫崖翡翠湖',meal:'清真餐·川菜',note:'无人区满油',hl:true},
 '冷湖':{name:'冷湖',lat:38.6300,lng:93.3200,alt:2800,temp:'9/-4',spots:'俄博梁雅丹 · 火星营地',meal:'自热饭·简餐',note:'砂石路四驱',hl:true},
 '敦煌':{name:'敦煌',lat:40.1421,lng:94.6616,alt:1138,temp:'20/6',spots:'莫高窟 · 鸣沙山月牙泉',meal:'驴肉黄面·杏皮水',note:'莫高窟提前约',hl:false},
 '嘉峪关':{name:'嘉峪关',lat:39.7731,lng:98.2905,alt:1600,temp:'18/5',spots:'嘉峪关关城 · 悬壁长城',meal:'烤肉·搓鱼面',note:'',hl:false},
 '酒泉':{name:'酒泉',lat:39.7436,lng:98.5105,alt:1477,temp:'18/5',spots:'西汉酒泉胜迹 · 酒泉公园 · 钟鼓楼',meal:'糊锅·羊肉粉汤',note:'东风航天城门户城市',hl:false},
 '东风航天城':{name:'东风航天城',lat:40.9616,lng:100.2258,alt:1000,temp:'15/0',spots:'问天阁 · 载人航天发射场 · 场史展览馆',meal:'东风宾馆·基地食堂',note:'军事管理区·参观需提前审批预约',hl:false},
 '张掖':{name:'张掖',lat:38.9258,lng:100.4522,alt:1480,temp:'17/4',spots:'大佛寺 · 木塔寺',meal:'炒拨拉·搓鱼面',note:'前往丹霞约40km',hl:false},
 '七彩丹霞':{name:'七彩丹霞',lat:38.9528,lng:100.0821,alt:1850,temp:'15/2',spots:'七彩云海台 · 七彩锦绣台 · 七彩虹霞台',meal:'景区简餐·出口农家乐',note:'日落色彩最艳·景区内禁飞无人机',hl:false},
 '祁连':{name:'祁连',lat:38.1833,lng:100.2500,alt:2800,temp:'12/-1',spots:'卓尔山 · 祁连草原',meal:'藏餐·牦牛酸奶',note:'垭口可能降雪',hl:false},
 '门源':{name:'门源',lat:37.3833,lng:101.6167,alt:2750,temp:'15/2',spots:'百里油菜花海 · 岗什卡雪峰',meal:'',note:'',hl:false},
 '日月山':{name:'日月山',lat:36.5500,lng:100.7500,alt:3520,temp:'8/-3',spots:'日月山垭口 · 文成公主庙 · 经幡',meal:'',note:'垭口风大·初上高原',hl:false},
 '茶卡':{name:'茶卡',lat:36.7833,lng:99.0833,alt:3100,temp:'11/1',spots:'茶卡盐湖 · 天空之镜',meal:'青盐·简餐',note:'晴天无风最佳',hl:false},
 '德令哈':{name:'德令哈',lat:37.3735,lng:97.3789,alt:2980,temp:'11/-1',spots:'可鲁克湖 · 柏树山',meal:'炕锅',note:'',hl:false},
 '当金山口':{name:'当金山口',lat:38.6167,lng:94.2500,alt:3640,temp:'6/-6',spots:'当金山垭口 · G215',meal:'',note:'翻越垭口·下坡长',hl:false},
 '阿克塞':{name:'阿克塞',lat:38.4667,lng:94.3000,alt:2800,temp:'9/-3',spots:'阿克塞石油小镇',meal:'',note:'',hl:false}
};
const LOC_KEYS=Object.keys(LOC_DB);
const DEFAULT_PLAN=[
 {date:'10/01',locs:['兰州'],fly:true},
 {date:'10/02',locs:['兰州','西宁']},
 {date:'10/03',locs:['西宁','日月山','青海湖','茶卡盐湖']},
 {date:'10/04',locs:['茶卡盐湖','德令哈','大柴旦']},
 {date:'10/05',locs:['大柴旦','水上雅丹']},
 {date:'10/06',locs:['水上雅丹','冷湖']},
 {date:'10/07',locs:['冷湖','敦煌']},
 {date:'10/08',locs:['敦煌']},
 {date:'10/09',locs:['敦煌','酒泉']},
 {date:'10/10',locs:['酒泉','东风航天城','张掖']},
 {date:'10/11',locs:['张掖','七彩丹霞','祁连']},
 {date:'10/12',locs:['祁连','门源','兰州']},
 {date:'10/13',locs:['兰州'],endFly:true}
];
const DEFAULT_BOOKINGS=__DEF_BOOKINGS__;
const DEFAULT_PACKING=__DEF_PACKING__;
const ROAD_FACTOR=1.25, FUEL_PER_KM=0.85;
let STOPS=[], DAY_COUNT=13;
function haversine(a,b){const R=6371,dLa=(b.lat-a.lat)*Math.PI/180,dLo=(b.lng-a.lng)*Math.PI/180,la1=a.lat*Math.PI/180,la2=b.lat*Math.PI/180;
 const h=Math.sin(dLa/2)**2+Math.cos(la1)*Math.cos(la2)*Math.sin(dLo/2)**2; return 2*R*Math.asin(Math.sqrt(h));}
function buildSTOPS(){
 const plan=state.plan||DEFAULT_PLAN; DAY_COUNT=plan.length; STOPS.length=0;
 plan.forEach(function(day,i){
  const locs=(day.locs&&day.locs.length)?day.locs.slice():(day.loc?[day.loc]:['兰州']);
  const pts=locs.map(function(n){ return LOC_DB[n]||LOC_DB['兰州']; });
  let km=0; for(let k=1;k<pts.length;k++){ km+=haversine(pts[k-1],pts[k]); } km=Math.round(km*ROAD_FACTOR);
  const lastPt=pts[pts.length-1];
  const stay=day.endFly?{name:'—',lat:lastPt.lat,lng:lastPt.lng,alt:'—',hl:false}:lastPt;
  const names=locs.map(function(n){ return LOC_DB[n]?LOC_DB[n].name:n; });
  let route=(day.fly?'上海 ✈ ':'')+names.join(' → ');
  if(day.endFly) route+=' → 上海 ✈';
  STOPS.push({d:i+1,name:stay.name,lat:stay.lat,lng:stay.lng,route:route,stay:stay.name,alt:String(stay.alt),km:km,hl:!!stay.hl,locs:locs.slice()});
 });
}
/* 同一住宿点出现多晚（如兰州住 D1+D12、敦煌住 D8+D9）时，坐标完全相同会叠在一起只显示最上层数字。
   按坐标分组，给同组每个标记一个水平偏移，使所有天数标签都能露出。 */
function groupStopOffsets(){
  const groups={}, order=[];
  STOPS.forEach(function(s,i){
    const key=s.lat.toFixed(5)+','+s.lng.toFixed(5);
    if(!groups[key]){ groups[key]=[]; order.push(key); }
    groups[key].push(i);
  });
  const res=new Array(STOPS.length);
  order.forEach(function(key){
    const arr=groups[key], n=arr.length;
    arr.forEach(function(idx,j){ res[idx]={n:n, j:j}; });
  });
  return res;
}
let _map=null,_markers=null,_info=null,_lmap=null,_lmarkers=null,_lroute=null,_polyline=null,_midMarkers=null;
function pinIcon(n,color){
  const svg="<svg xmlns='http://www.w3.org/2000/svg' width='34' height='44' viewBox='0 0 34 44'>"
    +"<path d='M17 0C7.6 0 0 7.6 0 17c0 12 17 27 17 27s17-15 17-27C34 7.6 26.4 0 17 0z' fill='"+color+"'/>"
    +"<circle cx='17' cy='17' r='12' fill='#fff'/>"
    +"<text x='17' y='22' font-size='15' font-family='Arial' font-weight='bold' text-anchor='middle' fill='"+color+"'>"+n+"</text></svg>";
  return 'data:image/svg+xml,'+encodeURIComponent(svg);
}
function initMap(){
  if(typeof TMap==='undefined'){console.warn('腾讯地图 SDK 未加载（可能处于离线/file:// 环境）');return;}
  _map=new TMap.Map('tmap',{zoom:5, center:new TMap.LatLng(36.6,99)});
  syncMap(); bindItineraryClicks(); fitRoute();
}
function initLeaflet(){
  if(typeof L==='undefined'){ console.warn('Leaflet 未加载，回退静态路线图'); showStaticRoute(); return; }
  _lmap=L.map('tmap',{scrollWheelZoom:true}).setView([36.6,99],5);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    maxZoom:18, attribution:'&copy; OpenStreetMap contributors'}).addTo(_lmap);
  syncMap(); bindItineraryClicks();
  var tip=document.querySelector('.map-tip');
  if(tip) tip.innerHTML='交互地图（OpenStreetMap，无需密钥，所有人可拖拽 / 缩放 / 点标记联动）。偏远无人区底图可能较稀疏；如需中国更精准底图，可接入高德 / 腾讯地图 key。';
}
function showStaticRoute(){
  var tw=document.querySelector('.tmap-wrap'); if(tw) tw.style.display='none';
  var s=document.getElementById('route-static'); if(s) s.style.display='block';
  var tip=document.querySelector('.map-tip');
  if(tip) tip.innerHTML='当前为离线视图：下方为路线示意图，行程卡片与海拔曲线均可正常使用。';
}
function focusStop(i){
  const s=STOPS[i]; if(!s) return;
  const html="<div style='min-width:190px;font-size:13px;line-height:1.7'>"
    +"<b style='font-size:15px'>D"+s.d+" · "+s.name+"</b><br>"
    +"<span style='color:#7d8a99'>"+s.route+"</span><br>"
    +"🏨 住宿："+s.stay+"<br>⛰ 海拔："+s.alt+" · 🚗 当日："+s.km+" km</div>";
  if(_map){
    _map.setCenter(new TMap.LatLng(s.lat,s.lng)); _map.setZoom(9);
    _info.setPosition(new TMap.LatLng(s.lat,s.lng)); _info.setContent(html); _info.open();
  } else if(_lmap){
    _lmap.setView([s.lat,s.lng], 9);
    L.popup({maxWidth:240}).setLatLng([s.lat,s.lng]).setContent(html).openOn(_lmap);
  }
}
function fitRoute(){
  const latlngs=STOPS.map(function(s){return [s.lat,s.lng];});
  if(_map){
    let minLat=90, maxLat=-90, minLng=180, maxLng=-180;
    STOPS.forEach(function(s){ minLat=Math.min(minLat,s.lat); maxLat=Math.max(maxLat,s.lat);
      minLng=Math.min(minLng,s.lng); maxLng=Math.max(maxLng,s.lng); });
    const b=new TMap.LatLngBounds(new TMap.LatLng(minLat,minLng), new TMap.LatLng(maxLat,maxLng));
    _map.fitBounds(b, {padding:50});
  } else if(_lmap){
    _lmap.fitBounds(L.latLngBounds(latlngs), {padding:[50,50]});
  }
}

/* ===== 行程总表 · 结构化编辑（只改日期/地点，其余自动推导） ===== */
function escA(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function renderItinerary(){
  const plan=state.plan||DEFAULT_PLAN; const list=document.getElementById('it-list'); if(!list) return;
  let html='';
  plan.forEach(function(day,i){
    const locs=(day.locs&&day.locs.length)?day.locs.slice():(day.loc?[day.loc]:['兰州']);
    const s=STOPS[i]||{route:'',km:0,alt:'0'};
    const fuel=Math.round((s.km||0)*FUEL_PER_KM);
    const stay=LOC_DB[locs[locs.length-1]]||LOC_DB['兰州'];
    const fly=day.fly?' <span class="tag-fly">✈ 飞抵</span>':(day.endFly?' <span class="tag-fly">✈ 返程</span>':'');
    let locHtml='';
    locs.forEach(function(n,k){
      const opts=LOC_KEYS.map(function(key){ return '<option value="'+key+'"'+(key===n?' selected':'')+'>'+LOC_DB[key].name+'</option>'; }).join('');
      const isMid=(k>0 && k<locs.length-1);
      const del=(isMid)?'<button class="it-delmid" data-day="'+i+'" data-idx="'+k+'" title="删除经停点">×</button>':'';
      const arr=(k>0)?'<span class="arr">→</span>':'';
      const role=(k===0)?'<span class="loc-role">出发</span>':((k===locs.length-1)?'<span class="loc-role">住宿</span>':'');
      locHtml+=arr+'<span class="loc-cell">'+role+'<select class="it-loc" data-day="'+i+'" data-idx="'+k+'">'+opts+'</select>'+del+'</span>';
    });
    const addMid='<button class="it-addmid" data-day="'+i+'">＋经停</button>';
    html+='<div class="tl-item" data-day="'+i+'">'
     +'<div class="tl-dot">D'+(i+1)+'</div>'
     +'<div class="tl-card">'
     +'<div class="tl-head"><input class="it-date" data-day="'+i+'" value="'+escA((DEFAULT_PLAN[i]?DEFAULT_PLAN[i].date:day.date))+'" readonly title="日期已固定，不可更改">'
     +'<span class="tl-km">约 '+s.km+' km · 油费≈¥'+fuel+'</span>'
     +'<label class="day-done"><input type="checkbox" id="day-'+i+'" class="ck"'+(state['day-'+i]?' checked':'')+' onchange="recompute()">完成</label></div>'
     +'<div class="tl-route-line"><span class="tl-route">'+escA(s.route)+'</span>'+fly+'</div>'
     +'<div class="tl-locs">'+locHtml+addMid+'</div>'
     +'<div class="tl-spots">'+escA(stay.spots)+'</div>'
     +'<div class="tl-foot">'
     +'<span class="tag-stay">🏨 '+escA(stay.name)+'</span>'
     +'<span class="tag-alt">⛰ '+escA(stay.alt)+'</span>'
     +'<span class="tag-temp">🌡 '+escA(stay.temp)+'</span>'
     +'<span class="tag-meal">🍽 '+escA(stay.meal)+'</span>'
     +'<span class="tag-note">'+escA(stay.note)+'</span>'
     +'</div></div></div>';
  });
  list.innerHTML=html;
}
function bindItineraryListeners(){
  const list=document.getElementById('it-list'); if(!list) return;
  list.querySelectorAll('.it-date').forEach(function(inp){ inp.addEventListener('input', function(e){
    const i=+e.target.dataset.day; if(!state.plan)state.plan=DEFAULT_PLAN.slice();
    state.plan[i]=state.plan[i]||{}; state.plan[i].date=e.target.value; save(); }); });
  list.querySelectorAll('.it-loc').forEach(function(sel){ sel.addEventListener('change', function(e){
    const i=+e.target.dataset.day, k=+e.target.dataset.idx; if(!state.plan)state.plan=DEFAULT_PLAN.slice();
    const day=state.plan[i]; if(!day.locs) day.locs=(day.loc?[day.loc]:['兰州']);
    day.locs[k]=e.target.value; day.loc=day.locs[day.locs.length-1];
    buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners(); syncMap(); save(); }); });
  list.querySelectorAll('.it-addmid').forEach(function(btn){ btn.addEventListener('click', function(e){
    const i=+e.target.dataset.day; if(!state.plan)state.plan=DEFAULT_PLAN.slice();
    const day=state.plan[i]; if(!day.locs) day.locs=(day.loc?[day.loc]:['兰州']);
    const k=day.locs.length-1; const prev=day.locs[k-1]||'西宁';
    day.locs.splice(k,0,prev); buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners(); syncMap(); save(); }); });
  list.querySelectorAll('.it-delmid').forEach(function(btn){ btn.addEventListener('click', function(e){
    const i=+e.target.dataset.day, k=+e.target.dataset.idx; if(!state.plan)state.plan=DEFAULT_PLAN.slice();
    const day=state.plan[i]; if(!day.locs) day.locs=(day.loc?[day.loc]:['兰州']);
    if(k>0 && k<day.locs.length-1){ day.locs.splice(k,1); buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners(); syncMap(); save(); } }); });
}
function bindItineraryClicks(){
  const list=document.getElementById('it-list'); if(!list||list._bc) return; list._bc=true;
  list.addEventListener('click', function(ev){
    if(ev.target && (ev.target.tagName==='INPUT'||ev.target.tagName==='SELECT')) return;
    const item=ev.target.closest('.tl-item'); if(!item) return; focusStop(+item.dataset.day);
  });
}
function syncMap(){
  const allPts=[]; STOPS.forEach(function(s){ (s.locs||[]).forEach(function(n){ const p=LOC_DB[n]||LOC_DB['兰州']; allPts.push([p.lat,p.lng]); }); });
  if(_lmap){
    (_lmarkers||[]).forEach(function(m){ _lmap.removeLayer(m); }); _lmarkers=[];
    STOPS.forEach(function(s){ const locs=s.locs||[]; for(let k=1;k<locs.length-1;k++){ const p=LOC_DB[locs[k]]||LOC_DB['兰州'];
      const ic=L.divIcon({className:'rw-pin',html:'<div style="background:#9aa7b4;color:#fff;width:14px;height:14px;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.3)"></div>',iconSize:[14,14],iconAnchor:[7,7]});
      _lmarkers.push(L.marker([p.lat,p.lng],{icon:ic}).addTo(_lmap)); } });
    const offs=groupStopOffsets();
    STOPS.forEach(function(s,i){ const color=s.hl?'#c97b5a':'#4a6d8c';
      const dx=(offs[i].n>1)?(offs[i].j-(offs[i].n-1)/2)*30:0;
      const icon=L.divIcon({className:'rw-pin',html:'<div style="background:'+color+';color:#fff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.35)">'+s.d+'</div>',iconSize:[26,26],iconAnchor:[13-dx,13]});
      _lmarkers.push(L.marker([s.lat,s.lng],{icon:icon}).addTo(_lmap).on('click', function(){ focusStop(i); })); });
    if(_lroute)_lmap.removeLayer(_lroute);
    _lroute=L.polyline(allPts,{color:'#4a6d8c',weight:5}).addTo(_lmap);
    if(allPts.length)_lmap.fitBounds(L.latLngBounds(allPts),{padding:[50,50]});
  } else if(_map){
    const styles={}, geoms=[], midStyles={}, midGeoms=[];
    const offs=groupStopOffsets();
    STOPS.forEach(function(s,i){ const color=s.hl?'#c97b5a':'#4a6d8c';
      const dx=(offs[i].n>1)?(offs[i].j-(offs[i].n-1)/2)*30:0;
      styles['s'+i]=new TMap.MarkerStyle({width:34,height:44,anchor:{x:17-dx,y:42},src:pinIcon(s.d,color)});
      geoms.push({id:'stop'+i,styleId:'s'+i,position:new TMap.LatLng(s.lat,s.lng),properties:{idx:i}}); });
    STOPS.forEach(function(s){ const locs=s.locs||[]; for(let k=1;k<locs.length-1;k++){ const p=LOC_DB[locs[k]]||LOC_DB['兰州'];
      const id='mid'+s.d+'_'+k; const ic='data:image/svg+xml,'+encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14'><circle cx='7' cy='7' r='5' fill='%239aa7b4' stroke='%23fff' stroke-width='2'/></svg>");
      midStyles[id]=new TMap.MarkerStyle({width:14,height:14,anchor:{x:7,y:7},src:ic});
      midGeoms.push({id:id,styleId:id,position:new TMap.LatLng(p.lat,p.lng)}); } });
    if(!_markers){ _markers=new TMap.MultiMarker({map:_map,styles:styles,geometries:geoms});
      _markers.on('click', function(e){ if(e&&e.geometry&&e.geometry.properties) focusStop(e.geometry.properties.idx); }); }
    else { _markers.setGeometries(geoms); }
    if(!_midMarkers){ _midMarkers=new TMap.MultiMarker({map:_map,styles:midStyles,geometries:midGeoms}); }
    else { _midMarkers.setGeometries(midGeoms); }
    const paths=allPts.map(function(pt){return new TMap.LatLng(pt[0],pt[1]);});
    if(!_polyline){ _polyline=new TMap.MultiPolyline({map:_map,styles:{r:new TMap.PolylineStyle({color:0x4a6d8cff,width:5,lineCap:'round',lineJoin:'round',borderWidth:1,borderColor:0xffffff})},geometries:[{id:'route',styleId:'r',paths:paths}]}); }
    else { _polyline.setGeometries([{id:'route',styleId:'r',paths:paths}]); }
    if(!_info)_info=new TMap.InfoWindow({map:_map,position:new TMap.LatLng(STOPS[0].lat,STOPS[0].lng),content:'',offset:{x:0,y:-30}});
    fitRoute();
  }
}
function nextDate(s){ let m=10,d=1; const mm=s&&s.match(/(\d{1,2})\/(\d{1,2})/); if(mm){m=+mm[1];d=+mm[2]+1; if(d>30){d=1;m++;}} return (m<10?'0':'')+m+'/'+(d<10?'0':'')+d; }
function addDay(){ if(!state.plan)state.plan=DEFAULT_PLAN.slice(); const last=state.plan[state.plan.length-1];
  const lastLoc=(last&&last.locs&&last.locs.length)?last.locs[last.locs.length-1]:(last&&last.loc?last.loc:'兰州');
  state.plan.push({date:nextDate(last?last.date:''),locs:[lastLoc]}); save(); buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners(); syncMap(); recompute(); }
function delDay(){ if(!state.plan)state.plan=DEFAULT_PLAN.slice(); if(state.plan.length<=1) return;
  state.plan.pop(); delete state['day-'+(state.plan.length)]; save(); buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners(); syncMap(); recompute(); }

/* ===== 预订管理 · 行李清单（可自由增减 / 编辑） ===== */
function readBookingRow(tr){
  const c=tr.children;
  return {item:c[0].querySelector('input').value, ch:c[1].querySelector('input').value,
    amt:c[2].querySelector('input').value, status:c[3].querySelector('select').value,
    dl:c[4].querySelector('input').value, owner:c[5].querySelector('input').value, note:c[6].querySelector('input').value};
}
function stCls(s){ return s==='已付'?'s-paid':(s==='已订'?'s-booked':'s-todo'); }
function updSt(el){ el.className='st '+stCls(el.value); }
/* 酒店预订随行程住宿点自动对齐：以行程每日「住宿」为唯一来源生成酒店行，
   用户手填的渠道/金额/状态等按「D{天} {城市}酒店」为键保留；改行程住宿即联动更新 */
var HOTEL_DEF={'兰州':{amt:320,note:'紧张'},'西宁':{amt:340,note:''},'青海湖':{amt:360,note:''},'茶卡盐湖':{amt:360,note:''},'大柴旦':{amt:380,note:''},'水上雅丹':{amt:420,note:'紧张'},'茫崖':{amt:360,note:'紧张'},'冷湖':{amt:300,note:''},'敦煌':{amt:400,note:''},'酒泉':{amt:320,note:''},'嘉峪关':{amt:320,note:''},'张掖':{amt:340,note:''},'祁连':{amt:300,note:''}};
function isHotelItem(s){ return /^D\d+ .*酒店$/.test(s||''); }
function syncHotelsFromItinerary(){
  if(!STOPS||!STOPS.length) return;
  if(!state.bookings) state.bookings=DEFAULT_BOOKINGS.map(function(b){return Object.assign({},b);});
  const custom=state.bookings.filter(function(b){return !isHotelItem(b.item);});
  const oldMap={}; state.bookings.forEach(function(b){ if(isHotelItem(b.item)) oldMap[b.item]=b; });
  const hotels=[];
  STOPS.forEach(function(s,i){
    if(!s.stay || s.stay==='—') return;
    const item='D'+(i+1)+' '+s.stay+'酒店';
    const prev=oldMap[item];
    if(prev){ hotels.push(Object.assign({},prev)); }
    else { const d=HOTEL_DEF[s.stay]||{amt:320,note:''};
      hotels.push({item:item, ch:'携程', amt:d.amt, status:'待订', dl:'9/15前', owner:'全员', note:d.note}); }
  });
  const pre=[], tickets=[];
  custom.forEach(function(b){ if(/机票|租车|往返|大交通/.test(b.item)) pre.push(b); else tickets.push(b); });
  state.bookings=pre.concat(hotels, tickets);
  renderBooking(); recompute(); save();
}
function renderBooking(){
  const list=document.getElementById('bk-list'); if(!list)return;
  const data=state.bookings||DEFAULT_BOOKINGS;
  list.innerHTML=data.map(function(b,idx){
    const sel=['已订','已付','待订'].map(function(s){return '<option value="'+s+'"'+(s===b.status?' selected':'')+'>'+s+'</option>';}).join('');
    const del='<button class="row-del" type="button" title="删除" onclick="delBooking('+idx+')">✕</button>';
    return '<tr data-owner="'+escA(b.owner||'')+'">'
      +'<td class="bk-item-cell"><input class="bk-in" value="'+escA(b.item||'')+'" placeholder="项目" oninput="recompute()">'+del+'</td>'
      +'<td><input class="bk-in" value="'+escA(b.ch||'')+'" placeholder="渠道" oninput="recompute()"></td>'
      +'<td class="num">¥<input class="bk-amt" value="'+(b.amt==null?0:b.amt)+'" inputmode="decimal" oninput="recompute()"></td>'
      +'<td><select class="st '+stCls(b.status)+'" onchange="updSt(this);recompute()">'+sel+'</select></td>'
      +'<td><input class="bk-in" value="'+escA(b.dl||'')+'" placeholder="截止" oninput="recompute()"></td>'
      +'<td><input class="bk-in" value="'+escA(b.owner||'')+'" placeholder="负责人" oninput="this.closest(\'tr\').dataset.owner=this.value;recompute()"></td>'
      +'<td><input class="bk-in" value="'+escA(b.note||'')+'" placeholder="备注" oninput="recompute()"></td>'
      +'</tr>';
  }).join('');
}
function addBooking(){ if(!state.bookings)state.bookings=DEFAULT_BOOKINGS.map(function(b){return Object.assign({},b);});
  state.bookings.push({item:'',ch:'',amt:0,status:'待订',dl:'',owner:'',note:''}); renderBooking(); recompute(); save(); }
function delBooking(idx){ if(!state.bookings)state.bookings=DEFAULT_BOOKINGS.map(function(b){return Object.assign({},b);});
  if(state.bookings.length<=1)return; state.bookings.splice(idx,1); renderBooking(); recompute(); save(); }

function readPackingRow(tr){
  const c=tr.children;
  return {cat:c[0].querySelector('input').value, item:c[1].querySelector('input').value,
    qty:c[2].querySelector('input').value, owner:c[3].querySelector('input').value, ok:c[4].querySelector('input').checked};
}
function renderPacking(){
  const list=document.getElementById('pk-list'); if(!list)return;
  const data=state.packing||DEFAULT_PACKING;
  list.innerHTML=data.map(function(p,idx){
    const del='<button class="row-del" type="button" title="删除" onclick="delPacking('+idx+')">✕</button>';
    return '<tr data-owner="'+escA(p.owner||'')+'">'
      +'<td><input class="bk-in" value="'+escA(p.cat||'')+'" placeholder="分类" oninput="recompute()"></td>'
      +'<td class="bk-item-cell"><input class="bk-in" value="'+escA(p.item||'')+'" placeholder="物品" oninput="recompute()">'+del+'</td>'
      +'<td><input class="bk-in" value="'+escA(p.qty||'')+'" placeholder="数量" oninput="recompute()"></td>'
      +'<td><input class="bk-in" value="'+escA(p.owner||'')+'" placeholder="负责人" oninput="this.closest(\'tr\').dataset.owner=this.value;recompute()"></td>'
      +'<td style="text-align:center"><input type="checkbox" class="ck"'+(p.ok?' checked':'')+' onchange="recompute()"></td>'
      +'</tr>';
  }).join('');
}
function addPacking(){ if(!state.packing)state.packing=DEFAULT_PACKING.map(function(p){return Object.assign({},p);});
  state.packing.push({cat:'',item:'',qty:'',owner:'蜜蜜',ok:false}); renderPacking(); recompute(); save(); }
function delPacking(idx){ if(!state.packing)state.packing=DEFAULT_PACKING.map(function(p){return Object.assign({},p);});
  if(state.packing.length<=1)return; state.packing.splice(idx,1); renderPacking(); recompute(); save(); }

/* ===== 导出/导入 JSON 备份（跨设备） ===== */
function exportJSON(){
  const inputs={pax:document.getElementById('pax').value, budget_plan:[], budget_paid:[], booking:[], bk_ch:[], bk_amt:[], packing:[], day:[]};
  for(let i=0;i<8;i++){inputs.budget_plan.push(document.getElementById('bd-plan-'+i).value);
    const pc=document.getElementById('bd-paid-'+i); inputs.budget_paid.push(pc.tagName==='INPUT'?pc.value:pc.textContent);}
  (state.bookings||[]).forEach(function(b){inputs.booking.push(b.item); inputs.bk_ch.push(b.ch); inputs.bk_amt.push(b.amt);});
  (state.packing||[]).forEach(function(p){inputs.packing.push(p.ok);});
  for(let i=0;i<DAY_COUNT;i++)inputs.day.push(document.getElementById('day-'+i).checked);
  const data={v:2, exported:new Date().toISOString(), state:state, inputs:inputs};
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download='大西北环线工作台备份_'+new Date().toISOString().slice(0,10)+'.json'; a.click();
  URL.revokeObjectURL(a.href);
}
function importJSON(input){
  const f=input.files[0]; if(!f) return;
  const r=new FileReader();
  r.onload=function(){
    try{
      const data=JSON.parse(r.result); state=data.state||{};
      const I=data.inputs||{};
      if(I.pax)document.getElementById('pax').value=I.pax;
      (I.budget_plan||[]).forEach(function(v,i){const el=document.getElementById('bd-plan-'+i); if(el)el.value=v;});
      (I.budget_paid||[]).forEach(function(v,i){const pc=document.getElementById('bd-paid-'+i); if(pc&&pc.tagName==='INPUT')pc.value=v;});
      if(I.booking&&I.booking.length)state.bookings=I.booking.map(function(v,i){return {item:v,ch:(I.bk_ch||[])[i]||'',amt:(I.bk_amt||[])[i]||0,status:'待订',dl:'',owner:'',note:''};});
      if(I.packing)state.packing=I.packing.map(function(v){return {cat:'',item:'',qty:'',owner:'蜜蜜',ok:!!v};});
      renderBooking(); renderPacking();
      (I.day||[]).forEach(function(v,i){const el=document.getElementById('day-'+i); if(el)el.checked=!!v;});
      save(); buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners(); recompute();
      alert('✅ 备份已导入，已恢复勾选与录入数据');
    }catch(e){alert('❌ 导入失败：'+e.message);}
  };
  r.readAsText(f); input.value='';
}

buildSTOPS();
syncHotelsFromItinerary();
renderItinerary();
bindItineraryListeners();
renderPacking();
recompute();
(function(){
  try{
    if(window._TMapSecurityConfig && /__WB_HTTP_PORT__/.test(window._TMapSecurityConfig.serviceHost)){
      initLeaflet();            // 非 WorkBuddy 预览（占位符未替换）→ 分享/公开视图：Leaflet 交互地图
    } else if(typeof TMap!=='undefined'){
      initMap();                // WorkBuddy 预览 → 腾讯实时地图
    } else {
      initLeaflet();
    }
  }catch(e){
    console.warn('优先地图初始化失败，尝试 Leaflet 兜底', e);
    try{ initLeaflet(); }catch(e2){ console.warn('Leaflet 也失败，启用静态路线图', e2); showStaticRoute(); }
  }
})();

/* ===== 共享状态同步（多人实时） ===== */
window.__sharedReady=false; window.__applyingRemote=false; window.__sharedVersion=0;
window.__cid=Math.random().toString(36).slice(2)+Date.now().toString(36);
window.SharedSync={
  init:function(){
    var self=this;
    fetch('/api/state',{cache:'no-store'}).then(function(r){return r.json();}).then(function(obj){
      if(obj && obj.state && Object.keys(obj.state).length){
        window.__applyingRemote=true;
        state=obj.state; window.__sharedVersion=obj.version||0;
        buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners();
        renderBooking(); renderPacking(); recompute(); syncMap();
        window.__applyingRemote=false;
      }
      window.__sharedReady=true; self._banner(true); self._subscribe();
    }).catch(function(){ window.__sharedReady=false; self._banner(false); });
  },
  _subscribe:function(){
    if(typeof EventSource==='undefined') return;
    var self=this;
    try{
      var es=new EventSource('/api/stream');
      es.addEventListener('update',function(ev){
        try{
          var obj=JSON.parse(ev.data);
          if(obj.from===window.__cid) return;                       // 忽略自己发出的回声
          if(!obj.state) return;
          if(obj.version && obj.version===window.__sharedVersion) return; // 双重保险
          window.__applyingRemote=true;
          state=obj.state; window.__sharedVersion=obj.version||0;
          buildSTOPS(); syncHotelsFromItinerary(); renderItinerary(); bindItineraryListeners();
          renderBooking(); renderPacking(); recompute(); syncMap();
          window.__applyingRemote=false;
        }catch(e){}
      });
      es.onerror=function(){};
    }catch(e){}
  },
  push:function(st){
    if(!window.__sharedReady || window.__applyingRemote) return;
    var self=this;
    if(this._t) clearTimeout(this._t);
    this._t=setTimeout(function(){
      fetch('/api/state',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({state:st,clientId:window.__cid})})
        .then(function(r){return r.json();}).then(function(o){ if(o&&o.version) window.__sharedVersion=o.version; })
        .catch(function(){});
    }, 700);
  },
  _banner:function(on){
    var el=document.getElementById('shared-banner'); if(!el) return;
    if(on){ el.className='shared-banner on'; el.textContent='🌐 已连接云端共享 · 你的改动会实时同步给所有人'; el.style.display='block'; }
    else { el.className='shared-banner off'; el.textContent='📱 本地模式（未检测到共享服务，改动仅存本机浏览器）'; el.style.display='block'; }
  }
};
SharedSync.init();
"""

JS2 = JS2.replace("__DEF_BOOKINGS__", _DEF_BOOKINGS_JSON).replace("__DEF_PACKING__", _DEF_PACKING_JSON)
HTML = HTML.replace("__JS2__", JS2)

path=r"大西北环线十三日自驾工作台.html"
with open(path,"w",encoding="utf-8") as f: f.write(HTML)
# 同时输出到 public/ 供后端服务托管
import os as _os
_pub=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"public")
if not _os.path.exists(_pub): _os.makedirs(_pub)
with open(_os.path.join(_pub,"index.html"),"w",encoding="utf-8") as f: f.write(HTML)
print("v2 generated:",len(HTML),"bytes ->",path,"| public/index.html")
