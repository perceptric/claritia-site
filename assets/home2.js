/* Home page: the try-it flow (brand learning, live form, routing, booking, emails), the scroll story and the dot globe. */
var NODES=[
  {ic:"form",c:"g",name:"New form submission",tag:'<span class="tag t-green">Book a demo</span>',pill:"Submitted"},
  {ic:"route",c:"b",name:"Round robin",tag:'<span class="tag t-blue">Sales, North America</span>',pill:"11 to 50"},
  {ic:"cal",c:"p",name:"Book a meeting",tag:'<span class="tag t-purple">Intro call</span><span class="tag t-gray">30 min</span>',pill:"Booked"},
  {ic:"spark",c:"o",name:"AI follow-up",tag:'<span class="tag t-orange">Demo booked</span><span class="tag t-gray">4 emails</span>',pill:""}
];
var RUN=["Triggering","Assigning","Opening calendar","Writing"];
function render(canvas,cur){
  var h="";
  NODES.forEach(function(n,k){
    var st=k<cur?"done":k===cur?"on":"todo";
    var label=k<cur?'<div class="status ok"><svg class="i s14"><use href="#nh-check"/></svg>Done</div>':k===cur?'<div class="status run"><span class="spin"></span>'+RUN[k]+'</div>':"";
    h+='<div class="nh-node '+st+'">'+label+'<div class="top"><span class="ic '+n.c+'"><svg class="i"><use href="#'+n.ic+'"/></svg></span>'+n.name+'<span class="nh-dots">⋮</span></div><div class="nh-sub">'+n.tag+'</div></div>';
    if(k<NODES.length-1)h+='<div class="wire'+(k<cur?" lit":"")+'">'+(k<cur&&n.pill?'<span class="pill">'+n.pill+'</span>':"")+'</div>';
  });
  canvas.querySelector(".rail").innerHTML=h;
  fill(canvas.querySelector(".slot-card"),cur);
}
function fill(slot,cur){
  slot.innerHTML="";slot.appendChild(document.getElementById("c"+cur).content.cloneNode(true));
  var g=slot.querySelector(".calgrid");
  if(g){var x="";["S","M","T","W","T","F","S"].forEach(function(d){x+='<div class="dn">'+d+'</div>'});
    var open=[16,17,18,19,20,23,24,25,30];
    for(var d=1;d<=30;d++){var c="d";if(open.indexOf(d)>-1)c+=" a";if(d===17)c+=" sel";x+='<div class="'+c+'"><span>'+d+'</span></div>'}
    g.innerHTML=x;}
}
// hero demo: pick a brand, Claritia learns its style, then the form, booking and AI email all run in that style
(function(){
  var AV={w44:"/assets/demo/women-44.jpg",w68:"/assets/demo/women-68.jpg",w65:"/assets/demo/women-65.jpg",w90:"/assets/demo/women-90.jpg",w26:"/assets/demo/women-26.jpg",m32:"/assets/demo/men-32.jpg",m46:"/assets/demo/men-46.jpg",m75:"/assets/demo/men-75.jpg"};
  function q(t){return "“"+t+"”"}
  var BRANDS=[
    {id:"pebble",name:"Pebble",industry:"Language app",
     logo:'<svg viewBox="0 0 24 24"><ellipse cx="12" cy="13" rx="10" ry="8" fill="currentColor"/><circle cx="8.5" cy="10.5" r="2" fill="#fff" opacity=".7"/></svg>',
     color:{accent:"#7c4dff",ink:"#5a2fd6",soft:"#efe9ff",bg:"#fffaf3",surface:"#ffffff",text:"#2b2340",muted:"#706886",line:"rgba(76,50,140,.16)"},
     font:{body:'"Nunito",sans-serif',head:'"Nunito",sans-serif',w:"800",tt:"none",ls:"-.01em",label:"Nunito, extra bold"},
     shape:{r:"16px",br:"16px",shadow:"0 4px 0 #5a2fd6",label:"Extra round, chunky buttons"},
     voice:"Let's goooo! You've totally got this.",
     form:{title:"Book a free lesson call",lede:"Tell us a bit about you and we'll match you with a tutor who gets you.",q:"Which language are you learning?",opts:["Spanish","French","Japanese","German"],need:"What's your goal?",ph:"Order food on my trip to Madrid",cta:"Let's go",confirm:"Book my lesson"},
     reps:[{n:"Lucía Romero",av:"w26"},{n:"Camille Durand",av:"w68"},{n:"Kenji Sato",av:"m46"},{n:"Jonas Weber",av:"m32"}],
     meet:"Free lesson call, 20 min",where:"Video call",
     match:function(r,o){return ["Meet your tutor, "+r.n,"Matched with a "+o+" tutor who has open spots this week."]},
     booked:function(st){return "You're all set, "+st.first+"!"},
     email:function(st,day,t){return {subj:"See you "+day+", "+st.first+"!",segs:[["Hey "+st.first+"!\n\nYour free lesson is locked in for "],[day+" at "+t,1],[". You want to "],[st.need?st.need.charAt(0).toLowerCase()+st.need.slice(1):"start speaking "+st.opt+" with confidence",1],[", so I'll bring a few fun "],[st.opt,1],[" phrases to get you there fast.\n\nCome as you are. Mistakes are part of the fun!\n\n"+st.rep.n.split(" ")[0]]]}}},
    {id:"maison",name:"Maison Vale",industry:"Luxury fashion",
     logo:'<svg viewBox="0 0 24 24"><rect x="2.5" y="2.5" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="12" y="15.6" text-anchor="middle" font-family="Playfair Display,serif" font-size="9.5" fill="currentColor">MV</text></svg>',
     color:{accent:"#1c1a17",ink:"#1c1a17",soft:"#f1ece2",bg:"#faf7f1",surface:"#fffdf9",text:"#1c1a17",muted:"#7b7366",line:"rgba(28,26,23,.18)"},
     font:{body:'"Jost",sans-serif',head:'"Playfair Display",serif',w:"500",tt:"none",ls:"0",label:"Playfair Display and Jost"},
     shape:{r:"0px",br:"0px",shadow:"none",label:"Sharp corners, flat buttons"},
     voice:"Considered. Timeless. Yours.",
     form:{title:"Reserve a private styling appointment",lede:"Share a few details and a stylist will prepare a selection for you.",q:"What is the occasion?",opts:["Wedding","Gala","Workwear","Travel"],need:"Anything we should know?",ph:"A navy suit, size 40",cta:"Continue",confirm:"Reserve"},
     reps:[{n:"Céline Marchand",av:"w65"},{n:"Hugo Laurent",av:"m75"},{n:"Inès Moreau",av:"w90"},{n:"Hugo Laurent",av:"m75"}],
     meet:"Private styling, 60 min",where:"The atelier",
     match:function(r,o){return ["Your stylist: "+r.n,"Paired with a stylist who specializes in "+o.toLowerCase()+"."]},
     booked:function(){return "Your appointment is reserved"},
     email:function(st,day,t){return {subj:"Your appointment at Maison Vale",segs:[["Dear "+st.first+",\n\nThank you for reserving "],[day+" at "+t,1],[" with us. Knowing it is for "],[st.opt.toLowerCase(),1],[", I will prepare a considered selection"],[st.need?", with "+q(st.need)+" in mind":"",1],[".\n\nChampagne will be waiting.\n\nWarm regards,\n"+st.rep.n]]}}},
    {id:"bright",name:"Brightside Dental",industry:"Dental clinic",
     logo:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor"/><path d="M7 13c1.6 2.6 8.4 2.6 10 0" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
     color:{accent:"#13a89e",ink:"#0b7c74",soft:"#e2f6f4",bg:"#f5fbfb",surface:"#ffffff",text:"#17333a",muted:"#5b7479",line:"rgba(19,90,96,.16)"},
     font:{body:'"DM Sans",sans-serif',head:'"DM Sans",sans-serif',w:"700",tt:"none",ls:"-.02em",label:"DM Sans"},
     shape:{r:"14px",br:"999px",shadow:"0 6px 14px -6px rgba(19,168,158,.6)",label:"Soft corners, pill buttons"},
     voice:"Gentle care and bright smiles.",
     form:{title:"Book your first visit",lede:"New here? Welcome! Tell us a little about you and we'll find the right dentist.",q:"What brings you in?",opts:["Checkup","Tooth pain","Whitening","Braces"],need:"Anything we should know?",ph:"A little nervous about dentists",cta:"Next",confirm:"Book my visit"},
     reps:[{n:"Dr. Amy Chen",av:"w90"},{n:"Dr. Marcus Reed",av:"m75"},{n:"Dr. Amy Chen",av:"w90"},{n:"Dr. Sofia Ruiz",av:"w44"}],
     meet:"New patient visit, 45 min",where:"Brightside, Main Street",
     match:function(r,o){return ["You'll see "+r.n,"Booked with the dentist who handles "+o.toLowerCase()+" visits."]},
     booked:function(st){return "See you soon, "+st.first},
     email:function(st,day,t){return {subj:"Getting ready for your visit",segs:[["Hi "+st.first+",\n\nWe're looking forward to seeing you on "],[day+" at "+t,1],[" for your "],[st.opt.toLowerCase()+" visit",1],[". "],[st.need?"You mentioned "+q(st.need)+". We'll take everything at your pace.":"We'll keep everything easy and calm.",1],["\n\nPlease bring your insurance card and arrive 10 minutes early.\n\nTake care,\n"+st.rep.n]]}}},
    {id:"north",name:"Northwind",industry:"B2B software",
     logo:'<svg viewBox="0 0 24 24"><path d="M12 2l8 20-8-5-8 5z" fill="currentColor"/></svg>',
     color:{accent:"#4f46e5",ink:"#3730a3",soft:"#eef0ff",bg:"#f8f9fc",surface:"#ffffff",text:"#111827",muted:"#6b7280",line:"rgba(17,24,39,.12)"},
     font:{body:'"Manrope",sans-serif',head:'"Manrope",sans-serif',w:"700",tt:"none",ls:"-.025em",label:"Manrope"},
     shape:{r:"8px",br:"8px",shadow:"0 1px 2px rgba(17,24,39,.3),inset 0 1px 0 rgba(255,255,255,.18)",label:"Crisp 8px corners"},
     voice:"Clear answers for busy teams.",
     form:{title:"Book a Northwind demo",lede:"Tell us about your team. We'll match you with the right person.",q:"How big is your team?",opts:["Just me","2 to 10","11 to 50","51 or more"],need:"What do you need help with?",ph:"Booking more demos from our site",cta:"Continue",confirm:"Confirm demo"},
     reps:[{n:"Sam Brooks",av:"m32",team:"the Starter team"},{n:"Sam Brooks",av:"m32",team:"the Starter team"},{n:"Maya Ortiz",av:"w44",team:"Sales, North America"},{n:"Lena Koch",av:"w68",team:"the Enterprise team"}],
     meet:"Product demo, 30 min",where:"Google Meet",
     match:function(r,o){return ["You'll meet "+r.n,"Routed by round robin to "+r.team+", because your team is "+o.toLowerCase()+"."]},
     booked:function(st){return "You're booked with "+st.rep.n.split(" ")[0]},
     email:function(st,day,t){var team={"Just me":"a team of one","2 to 10":"a small team like yours","11 to 50":"a team of 11 to 50","51 or more":"a larger team like yours"}[st.opt];
       return {subj:"Ideas for our call on "+day,segs:[["Hi "+st.first+",\n\nThanks for booking time on "],[day+" at "+t,1],[". You want help with "],[st.need?q(st.need):"booking more meetings from your site",1],[", so I'll come ready with ideas that work for "],[team,1],[".\n\nI'll also show how round robin keeps every lead with the right rep.\n\nTalk soon,\n"+st.rep.n.split(" ")[0]]]}}},
    {id:"ridge",name:"Ridgeline Roofing",industry:"Home services",
     logo:'<svg viewBox="0 0 24 24"><path d="M2 13L12 4l10 9" stroke="currentColor" stroke-width="3" fill="none"/><rect x="6" y="13" width="12" height="8" fill="currentColor"/></svg>',
     color:{accent:"#f26b1d",ink:"#b9500f",soft:"#fff0e4",bg:"#f6f4f1",surface:"#ffffff",text:"#1f2328",muted:"#5f6368",line:"rgba(31,35,40,.16)"},
     font:{body:'"Barlow",sans-serif',head:'"Barlow Condensed",sans-serif',w:"700",tt:"uppercase",ls:".01em",label:"Barlow Condensed, bold caps"},
     shape:{r:"4px",br:"4px",shadow:"0 3px 0 #1f2328",label:"Square corners, solid buttons"},
     voice:"Straight talk. Solid roofs.",
     form:{title:"Get a free roof estimate",lede:"Tell us about the job. The closest crew lead will come take a look.",q:"What do you need?",opts:["Repair","New roof","Inspection","Storm damage"],need:"Anything else?",ph:"Leak over the kitchen since the storm",cta:"Next step",confirm:"Book my visit"},
     reps:[{n:"Dan Miller",av:"m75"},{n:"Tony Reyes",av:"m46"},{n:"Dan Miller",av:"m75"},{n:"Tony Reyes",av:"m46"}],
     meet:"Free on-site estimate, 45 min",where:"At your home",
     match:function(r,o){return [r.n+" will come out","Sent to the closest crew lead for "+o.toLowerCase()+" jobs."]},
     booked:function(st){return "You're on the schedule, "+st.first},
     email:function(st,day,t){return {subj:"Your roof estimate on "+day,segs:[["Hi "+st.first+",\n\nThanks for booking. I'll be out on "],[day+" at "+t,1],[" to look at your "],[st.opt.toLowerCase(),1],[" job. "],[st.need?"You mentioned "+q(st.need)+", so I'll check that first.":"I'll check the whole roof while I'm up there.",1],["\n\nThe visit is free, and you'll get a written quote the same day.\n\nSee you then,\n"+st.rep.n.split(" ")[0]]]}}}
  ];
  // per-brand show-if logic, live calculator and marketing emails
  function money(n,cur){return (cur||"$")+Math.round(n).toLocaleString("en-US")}
  var EXTRA={
    pebble:{
      logic:function(i,o){return i===2?{q:"Can you read hiragana yet?",opts:["Not yet","A little","Yes"]}:{q:"Have you studied "+o+" before?",opts:["Never","A little","A lot"]}},
      calc:{label:"Lessons per week",min:1,max:5,step:1,val:2,show:function(v){return v+(v>1?" lessons":" lesson")},total:function(v){return money(v*12*4)+" / month"},note:"$12 a lesson, billed monthly"},
      mails:{confirm:{subj:"Your lesson is booked!",head:"Your lesson is booked!",body:"Get ready to say your first {opt} words with {rep}. It's going to be fun.",btn:"Add to calendar"},
             remind:{subj:"Tomorrow's the day, {first}",head:"Tomorrow's the day!",body:"Your free lesson with {rep} starts {when}. Find a quiet spot and bring your voice.",btn:"Join the call"},
             news:{subj:"5 {opt} phrases for this week",head:"5 phrases to learn this week",body:"Tiny lessons, big wins. Here are this week's favorite {opt} phrases, picked by our tutors.",btn:"Start learning"}}},
    maison:{
      logic:function(i){return [{q:"Are you the one getting married?",opts:["Yes","I'm a guest"]},{q:"Is it black tie?",opts:["Yes","Not sure","No"]},{q:"How formal is your office?",opts:["Suit and tie","Smart casual","Relaxed"]},{q:"Where are you headed?",opts:["City","Coast","Mountains"]}][i]},
      calc:{label:"Number of looks",min:1,max:6,step:1,val:3,show:function(v){return v+(v>1?" looks":" look")},total:function(v){return "From "+money(v*450)},note:"Our stylists build each look around you"},
      mails:{confirm:{subj:"Your appointment is reserved",head:"We look forward to welcoming you",body:"Your private styling for {opt} is reserved for {when}. {rep} is preparing your selection.",btn:"View appointment"},
             remind:{subj:"Tomorrow at Maison Vale",head:"Until tomorrow",body:"{rep} will meet you at the atelier {when}. Bring a favorite piece if you like.",btn:"Get directions"},
             news:{subj:"The autumn edit",head:"The autumn edit",body:"Twelve new pieces, made in small runs. Reserve a private viewing before they are gone.",btn:"See the edit"}}},
    bright:{
      logic:function(i){return [{q:"When was your last cleaning?",opts:["Under a year","1 to 2 years","Longer"]},{q:"How bad is the pain?",opts:["Mild","Strong","Severe"]},{q:"Have you whitened before?",opts:["Yes","No"]},{q:"Who are the braces for?",opts:["Me","My child"]}][i]},
      calc:{label:"Insurance covers",min:0,max:100,step:10,val:80,show:function(v){return v+"%"},total:function(v){return "You pay about "+money(180*(100-v)/100)},note:"Visit price before insurance: $180"},
      mails:{confirm:{subj:"You're booked at Brightside",head:"You're booked!",body:"Your {opt} visit with {rep} is set for {when}. We'll keep it calm and easy.",btn:"Add to calendar"},
             remind:{subj:"See you tomorrow, {first}",head:"See you tomorrow",body:"Your visit with {rep} is {when}. Bring your insurance card and arrive 10 minutes early.",btn:"Confirm visit"},
             news:{subj:"3 habits for a brighter smile",head:"3 habits for a brighter smile",body:"Small habits make a big difference. Here are three our team swears by.",btn:"Read the tips"}}},
    north:{
      logic:function(i){return i<2?{q:"Do you use a CRM today?",opts:["HubSpot","Salesforce","Other","None"]}:{q:"How many reps share leads?",opts:["2 to 5","6 to 20","21 or more"]}},
      calc:{label:"Seats",min:1,max:50,step:1,val:10,show:function(v){return v+(v>1?" seats":" seat")},total:function(v){return money(v*19)+" / month"},note:"$19 a seat, billed monthly"},
      mails:{confirm:{subj:"Your Northwind demo is confirmed",head:"Your demo is confirmed",body:"You'll meet {rep} {when}. We'll tailor it to a team that's {opt}.",btn:"Add to calendar"},
             remind:{subj:"Your demo is tomorrow",head:"See you tomorrow",body:"Your demo with {rep} is {when}. Bring your questions and a teammate or two.",btn:"Join Google Meet"},
             news:{subj:"What's new in Northwind",head:"What's new this month",body:"Faster reports, smarter routing and a new Slack app. Here's everything we shipped.",btn:"See what's new"}}},
    ridge:{
      logic:function(i){return [{q:"Where is the problem?",opts:["Leak","Missing shingles","Gutters"]},{q:"What material do you want?",opts:["Shingle","Metal","Tile"]},{q:"Are you buying or selling?",opts:["Buying","Selling","Neither"]},{q:"Is water coming in right now?",opts:["Yes","No"]}][i]},
      calc:{label:"Roof size",min:800,max:4000,step:100,val:2000,show:function(v){return v.toLocaleString("en-US")+" sq ft"},total:function(v){return money(v*4.5)+" to "+money(v*6.5)},note:"Rough range. Your crew lead confirms on site"},
      mails:{confirm:{subj:"Your estimate is booked",head:"You're on the schedule",body:"{rep} will come out {when} to look at your {opt} job. The visit is free.",btn:"Add to calendar"},
             remind:{subj:"We're coming tomorrow",head:"See you tomorrow",body:"{rep} will be there {when}. Please make sure we can get to the side of the house.",btn:"Reschedule"},
             news:{subj:"Get your roof ready for winter",head:"Ready for winter?",body:"Five quick checks that stop leaks before the first big storm.",btn:"Get the checklist"}}}
  };
  BRANDS.forEach(function(b){var x=EXTRA[b.id];b.logic=x.logic;b.calc=x.calc;b.mails=x.mails});
  var TIMES=["9:00 am","9:30 am","10:30 am","11:00 am","1:00 pm","2:30 pm","3:00 pm","4:30 pm"];
  var tb=document.getElementById("tb"),form=document.getElementById("tf");
  var steps=["s0","s1","tf","ts1","ts2"].map(function(id){return document.getElementById(id)});
  var prog=[].slice.call(document.querySelectorAll(".try-prog span")),PROG=[0,0,1,2,3];
  var calm=matchMedia("(prefers-reduced-motion: reduce)").matches;
  var brand=null,st={},days=[],dayI=0,timeI=-1,timers=[],typer=null;
  function $(id){return document.getElementById(id)}
  function later(fn,ms){timers.push(setTimeout(fn,calm?0:ms))}
  function clearAll(){timers.forEach(clearTimeout);timers=[];clearInterval(typer)}
  function show(i){steps.forEach(function(el,k){el.hidden=k!==i});prog.forEach(function(p,k){p.classList.toggle("on",k<=PROG[i])})}
  var tz="your time zone";try{tz=(Intl.DateTimeFormat().resolvedOptions().timeZone||"").split("/").pop().replace(/_/g," ")||tz}catch(e){}
  $("tz").textContent=tz;

  function setVars(el,b,part){
    var c=b.color,f=b.font,sh=b.shape,v={};
    if(part==="color"||part==="all")v={"--b-accent":c.accent,"--b-ink":c.ink,"--b-soft":c.soft,"--b-bg":c.bg,"--b-surface":c.surface,"--b-text":c.text,"--b-muted":c.muted,"--b-line":c.line};
    if(part==="font"||part==="all"){v["--b-font"]=f.body;v["--b-head"]=f.head;v["--b-head-w"]=f.w;v["--b-head-tt"]=f.tt;v["--b-head-ls"]=f.ls}
    if(part==="shape"||part==="all"){v["--b-r"]=sh.r;v["--b-br"]=sh.br;v["--b-btn-shadow"]=sh.shadow}
    for(var k in v)el.style.setProperty(k,v[k]);
  }
  function resetVars(){tb.removeAttribute("style")}
  function logo(b){return b.logo+"<span>"+b.name+"</span>"}

  // brand tiles, each drawn in its own style
  var h="";BRANDS.forEach(function(b,i){h+='<button type="button" class="bt" data-i="'+i+'"><span class="blogo">'+logo(b)+'</span><span class="bar">'+b.form.cta+'</span><small>'+b.industry+'</small></button>'});
  $("brands").innerHTML=h;
  [].forEach.call(document.querySelectorAll(".bt"),function(el){setVars(el,BRANDS[+el.dataset.i],"all")});
  $("brands").addEventListener("click",function(e){var t=e.target.closest(".bt");if(t)learn(BRANDS[+t.dataset.i])});

  function learn(b){
    clearAll();brand=b;resetVars();show(1);$("swap").hidden=false;
    $("learn").hidden=false;$("like").hidden=true;$("ln-name").textContent=b.name;$("ln-spin").style.display="";
    var li=[].slice.call(document.querySelectorAll(".lsteps li"));li.forEach(function(x){x.classList.remove("done")});
    ["lv0","lv1","lv2","lv3"].forEach(function(id){$(id).innerHTML=""});
    var c=b.color;
    later(function(){setVars(tb,b,"color");li[0].classList.add("done");$("lv0").innerHTML=[c.accent,c.soft,c.text,c.bg].map(function(x){return '<span class="dot" style="background:'+x+'"></span>'}).join("")},650);
    later(function(){setVars(tb,b,"font");li[1].classList.add("done");$("lv1").textContent=b.font.label},1300);
    later(function(){setVars(tb,b,"shape");li[2].classList.add("done");$("lv2").textContent=b.shape.label},1950);
    later(function(){li[3].classList.add("done");$("lv3").innerHTML="<i>"+q(b.voice)+"</i>";$("ln-spin").style.display="none"},2600);
    later(function(){
      $("learn").hidden=true;$("like").hidden=false;$("lk-logo").innerHTML=logo(b);$("lk-btn").textContent=b.form.cta;
      $("lk-sw").innerHTML=[c.accent,c.soft,c.text].map(function(x){return '<i style="background:'+x+'"></i>'}).join("");
      $("like-go").focus({preventScroll:true});
    },3400);
  }
  $("like-go").onclick=function(){buildForm();show(2);$("try-name").focus({preventScroll:true})};
  $("like-other").onclick=$("swap").onclick=$("restart").onclick=function(){clearAll();resetVars();brand=null;$("swap").hidden=true;show(0)};

  function buildForm(){
    var f=brand.form;form.reset();
    $("f-logo").innerHTML=logo(brand);$("f-title").textContent=f.title;$("f-lede").textContent=f.lede;$("f-q").textContent=f.q;
    $("f-need").textContent=f.need;$("try-need").placeholder=f.ph;$("f-cta").textContent=f.cta;
    $("f-opts").innerHTML=f.opts.map(function(o,i){return '<input type="radio" name="opt" id="op'+i+'" value="'+i+'"><label for="op'+i+'">'+o+'</label>'}).join("");
    var c=brand.calc;$("f-logic").hidden=true;$("f-logic").innerHTML="";
    $("f-calc").innerHTML='<div class="calc-top"><label for="try-calc">'+c.label+'</label><span class="calc-chip"><svg class="i s12"><use href="#nh-calc"/></svg>Calculated live</span></div>'+
      '<div class="calc-row"><input type="range" id="try-calc" min="'+c.min+'" max="'+c.max+'" step="'+c.step+'" value="'+c.val+'"><output id="calc-v"></output></div>'+
      '<div class="calc-total"><span><small>Estimate</small><b id="calc-t"></b></span><small>'+c.note+'</small></div>';
    calcUpdate();
    ["err-name","err-email","err-opt"].forEach(function(id){$(id).textContent=""});
    form.querySelectorAll(".bad").forEach(function(x){x.classList.remove("bad")});
  }
  function calcUpdate(){var el=$("try-calc");if(!el)return;var v=+el.value;$("calc-v").textContent=brand.calc.show(v);var t=$("calc-t");t.textContent=brand.calc.total(v);t.classList.remove("bump");void t.offsetWidth;t.classList.add("bump")}
  function showLogic(i){
    var l=brand.logic(i,brand.form.opts[i]),box=$("f-logic");
    if(!l){box.hidden=true;box.innerHTML="";return}
    box.innerHTML='<span class="logic-badge"><svg class="i s12"><use href="#nh-branch"/></svg>Logic: shown because you picked '+q(brand.form.opts[i])+'</span><label>'+l.q+'</label><div class="rchoices lg">'+
      l.opts.map(function(o,k){return '<input type="radio" name="lg" id="lg'+k+'" value="'+o+'"><label for="lg'+k+'">'+o+'</label>'}).join("")+'</div>';
    box.hidden=false;box.classList.remove("in");void box.offsetWidth;box.classList.add("in");
  }
  form.addEventListener("input",function(e){if(e.target.id==="try-calc")calcUpdate()});
  function err(id,msg,input){$(id).textContent=msg;if(input)input.classList.toggle("bad",!!msg)}
  form.addEventListener("submit",function(e){
    e.preventDefault();
    var n=form.elements.name,em=form.elements.email,op=form.querySelector('input[name="opt"]:checked'),ok=true;
    if(!n.value.trim()){err("err-name","Add your name so we know who's coming.",n);ok=false}else err("err-name","",n);
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em.value.trim())){err("err-email","Enter an email like jane@email.com.",em);ok=false}else err("err-email","",em);
    if(!op){err("err-opt","Pick one. It decides who you'll meet.");ok=false}else err("err-opt","");
    if(!ok){(form.querySelector(".bad")||form.querySelector('input[name="opt"]')).focus();return}
    var i=+op.value;
    st={name:n.value.trim(),first:n.value.trim().split(/\s+/)[0],email:em.value.trim(),opt:brand.form.opts[i],need:form.elements.need.value.trim(),rep:brand.reps[i],lg:(form.querySelector('input[name="lg"]:checked')||{}).value||"",est:$("calc-t").textContent,estLabel:brand.calc.show(+$("try-calc").value)};
    route();
  });
  ["try-name","try-email"].forEach(function(id){$(id).addEventListener("input",function(){this.classList.remove("bad");$("err-"+id.slice(4)).textContent=""})});
  form.addEventListener("change",function(e){if(e.target.name==="opt"){err("err-opt","");showLogic(+e.target.value)}});

  function route(){
    show(3);var m=$("match");$("pick").hidden=true;m.className="match wait";
    m.innerHTML='<span class="spin"></span><div><b>Finding the right person…</b><small>Checking your answer: '+st.opt+'</small></div>';
    later(function(){
      var t=brand.match(st.rep,st.opt);m.className="match";
      m.innerHTML='<img src="'+AV[st.rep.av]+'" alt=""><div><b>'+t[0]+'</b><small>'+t[1]+'</small></div>';
      $("m-name").textContent=brand.meet;$("m-where").textContent=brand.where;$("c-cta").textContent=brand.form.confirm;
      dayI=0;timeI=-1;buildDays();$("pick").hidden=false;
    },1100);
  }
  function buildDays(){
    days=[];var d=new Date();d.setHours(12,0,0,0);
    while(days.length<5){d.setDate(d.getDate()+1);if(d.getDay()%6)days.push(new Date(d))}
    $("days").innerHTML=days.map(function(x,k){return '<button type="button" class="day'+(k===dayI?" sel":"")+'" data-k="'+k+'"><small>'+x.toLocaleDateString("en-US",{weekday:"short"})+'</small><b>'+x.getDate()+'</b></button>'}).join("");
    buildTimes();
  }
  function buildTimes(){
    $("times").innerHTML=TIMES.map(function(t,k){var taken=(dayI*3+k)%4===0;return '<button type="button" class="tm'+(k===timeI?" sel":"")+'" data-k="'+k+'"'+(taken?' disabled aria-label="'+t+', taken"':'')+'>'+t+'</button>'}).join("");
    $("confirm").disabled=timeI<0;
  }
  $("days").addEventListener("click",function(e){var b=e.target.closest(".day");if(!b)return;dayI=+b.dataset.k;timeI=-1;buildDays()});
  $("times").addEventListener("click",function(e){var b=e.target.closest(".tm");if(!b||b.disabled)return;timeI=+b.dataset.k;buildTimes()});
  $("back").onclick=function(){show(2);$("try-name").focus({preventScroll:true})};
  $("confirm").onclick=book;

  function book(){
    if(timeI<0)return;
    var day=days[dayI],dLong=day.toLocaleDateString("en-US",{weekday:"long",month:"long",day:"numeric"}),dShort=day.toLocaleDateString("en-US",{weekday:"long"}),t=TIMES[timeI];
    show(4);
    $("bk-title").textContent=brand.booked(st);
    $("bk-when").textContent=brand.meet.split(",")[0]+" on "+dLong+" at "+t+" ("+tz+"). The invite is on its way to "+st.email+".";
    $("em-to").textContent=st.name;$("em-from").textContent=st.rep.n;$("em-av").src=AV[st.rep.av];
    $("bk-est").innerHTML='<svg class="i s12"><use href="#nh-calc"/></svg>'+brand.calc.label+": "+st.estLabel+" · "+st.est;
    var e=brand.email(st,dShort,t);$("em-subj").textContent=e.subj;type($("em-body"),e.segs);
    st.when=dShort+" at "+t;tab("ai");
  }
  function fillT(s){return s.replace(/\{(\w+)\}/g,function(m,k){return {opt:st.opt,rep:st.rep.n,first:st.first,when:st.when}[k]||""})}
  function tab(k){
    [].forEach.call(document.querySelectorAll(".em-tab"),function(b){var on=b.dataset.t===k;b.classList.toggle("on",on);b.setAttribute("aria-selected",on)});
    $("em-ai").hidden=k!=="ai";$("em-view").hidden=k==="ai";
    if(k==="ai")return;
    var m=brand.mails[k];
    $("em-view").innerHTML='<div class="mrow">From <b>'+brand.name+'</b><span style="margin-left:auto">To '+st.name+'</span></div><div class="mrow">Subject <b>'+fillT(m.subj)+'</b></div>'+
      '<div class="paper-wrap"><div class="paper"><div class="paper-top"><span class="blogo">'+logo(brand)+'</span></div>'+
      '<div class="paper-hero"><h4>'+fillT(m.head)+'</h4></div><div class="paper-body"><p>Hi '+st.first+',</p><p>'+fillT(m.body)+'</p><span class="tbtn paper-btn">'+m.btn+'</span></div>'+
      '<div class="paper-foot">You get this email because you booked with '+brand.name+'. Unsubscribe</div></div></div>';
  }
  document.getElementById("em-tabs").addEventListener("click",function(e){var b=e.target.closest(".em-tab");if(b)tab(b.dataset.t)});
  function type(el,segs){
    clearInterval(typer);el.innerHTML="";var state=$("ai-state");state.textContent="Writing…";state.className="tag2 warm";
    var spans=segs.map(function(sg){var sp=document.createElement("span");if(sg[1])sp.className="hl";el.appendChild(sp);return sp});
    function done(){el.classList.remove("go");state.textContent="Ready to send";state.className="tag2 ok"}
    if(calm){segs.forEach(function(sg,i){spans[i].textContent=sg[0]});done();return}
    el.classList.add("go");var i=0,j=0;
    typer=setInterval(function(){for(var n=0;n<3;n++){while(i<segs.length&&!segs[i][0].length)i++;if(i>=segs.length){clearInterval(typer);done();return}
      spans[i].textContent+=segs[i][0].charAt(j++);if(j>=segs[i][0].length){i++;j=0}}},16);
  }
})();
// story: scroll progress through the pinned section picks the step
var storyEl=document.getElementById("story"),storyCanvas=document.getElementById("storyCanvas");
var steps=[].slice.call(document.querySelectorAll(".stp")),navs=[].slice.call(document.querySelectorAll(".sn")),shown=-1;
steps.forEach(function(s,k){fill(s.querySelector(".m-card"),k)});
function setStep(i){if(i===shown)return;shown=i;
  steps.forEach(function(s,k){s.classList.toggle("on",k===i)});
  navs.forEach(function(n,k){n.classList.toggle("on",k===i)});
  render(storyCanvas,i)}
function progress(){var r=storyEl.getBoundingClientRect(),run=storyEl.offsetHeight-storyEl.querySelector(".pin").offsetHeight;
  return run>0?Math.min(1,Math.max(0,-r.top/run)):0}
function onScroll(){if(getComputedStyle(storyEl.querySelector(".pin")).position!=="sticky")return;
  var p=progress(),n=steps.length;setStep(Math.min(n-1,Math.floor(p*n)));
  navs.forEach(function(el,k){var f=Math.min(1,Math.max(0,p*n-k));el.style.setProperty("--fill",(f*100).toFixed(1)+"%")})}
navs.forEach(function(el,k){el.onclick=function(){var run=storyEl.offsetHeight-storyEl.querySelector(".pin").offsetHeight;
  var top=storyEl.getBoundingClientRect().top+scrollY;scrollTo({top:top+run*(k+.5)/steps.length,behavior:"smooth"})}});
setStep(0);onScroll();
addEventListener("scroll",onScroll,{passive:true});addEventListener("resize",onScroll);
// pills
[].forEach.call(document.querySelectorAll(".pill-b"),function(b){b.onclick=function(){[].forEach.call(document.querySelectorAll(".pill-b"),function(o){o.classList.remove("on")});b.classList.add("on")}});
// final: a dot globe with the Claritia mark, a slow ripple and bookings that light up
(function(){
  var c=document.getElementById("orb");if(!c)return;
  var ctx=c.getContext("2d"),W,H,R,cx,cy,dots=[],dpr=Math.min(2,window.devicePixelRatio||1);
  var still=/[?&]still=/.test(location.search)||matchMedia("(prefers-reduced-motion: reduce)").matches;
  function inMark(x,y){ // Claritia mark: rounded tile with four pills, in unit space -1..1
    var pills=[[-.62,-.42,.36,.26],[.04,-.42,.58,.26],[-.62,.16,.58,.26],[.26,.16,.36,.26]];
    for(var i=0;i<pills.length;i++){var p=pills[i];if(x>p[0]&&x<p[0]+p[2]&&y>p[1]&&y<p[1]+p[3])return 2}
    return Math.abs(x)<.86&&Math.abs(y)<.86?1:0;
  }
  function setup(){
    var r=c.getBoundingClientRect();W=r.width;H=r.height;c.width=W*dpr;c.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);
    R=Math.min(W*.42,H*.92);cx=W/2;cy=H*1.0;dots=[];var g=W<600?7:8.5;
    for(var y=cy-R;y<H;y+=g)for(var x=cx-R;x<cx+R;x+=g){
      var dx=(x-cx)/R,dy=(y-cy)/R,d2=dx*dx+dy*dy;if(d2>1)continue;
      var z=Math.sqrt(1-d2),light=Math.max(0,(-dx*.35-dy*.75+z*.6));
      var mx=dx/0.40,my=(dy+.56)/0.40,m=inMark(mx,my);
      dots.push({x:x,y:y,d:Math.sqrt(d2),l:light,m:m,ph:Math.random()*6.28,b:0});
    }
  }
  var t=0;
  function frame(){
    ctx.clearRect(0,0,W,H);t+=.016;
    if(!still&&dots.length&&Math.random()<.35){var k=dots[(Math.random()*dots.length)|0];if(k&&k.m===0)k.b=1}
    for(var i=0;i<dots.length;i++){var p=dots[i];
      var wave=.5+.5*Math.sin(p.d*18-t*2.2);
      var fade=Math.min(1,(H-p.y)/(H*.55));
      var a,col,sz;
      if(p.m===2){col="8,100,68";a=.95;sz=2.2}
      else if(p.m===1){col="12,140,94";a=.22+.25*wave;sz=1.7}
      else if(p.b>.02){col="12,140,94";a=p.b;sz=1.6+p.b*1.4;p.b*=.965}
      else{col="60,60,55";a=(.06+.32*p.l)*(.65+.35*wave);sz=1.1+.9*p.l}
      ctx.fillStyle="rgba("+col+","+(a*fade).toFixed(3)+")";
      ctx.beginPath();ctx.arc(p.x,p.y,sz,0,6.283);ctx.fill();
    }
    if(!still)requestAnimationFrame(frame);
  }
  setup();frame();
  window.addEventListener("resize",function(){setup();if(still)frame()});
})();
