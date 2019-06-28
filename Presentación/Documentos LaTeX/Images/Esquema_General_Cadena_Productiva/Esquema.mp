
%-----ESQUEMA GENERAL------
beginfig(1);
%Datos del rectangulo
h = 1.5cm;
ancho = 3cm;

%Label - Entradas
pair p[], O[], Origen;
O0 =  (0,1cm); O1 = (0, 0.5cm); O2 = (1.3cm,1cm);
label("Plant", O0);
label("material", O1);
label("Input", O2);


%Flecha
Origen = 0.8cm*right;
l_flecha = 1cm;
p0 = (xpart Origen,0.5*h); p1 = (xpart Origen + l_flecha,0.5h);
drawarrow p0--p1 withcolor green;


%Rectángulo
pair l[];
x = xpart Origen + l_flecha;
l0 = (x,0); l1 = (x+ancho,0); l2 = (x+ancho,h); l3 = (x,h);
draw 
	for i=0 upto 3:
		l[i]--
	endfor
cycle withcolor green;

%Label dentro del rectángulo
pair centro_rectangulo;
centro_rectangulo = (((x+ancho)/2)+0.85cm,h/2);
label("Biofactory", centro_rectangulo) withcolor green;

%Salida
pair line[], s[], ss[], sss[], t, tt, ttt, tttt;
px = xpart Origen + l_flecha + ancho;
fin = px+l_flecha+0.25cm;
line0 = (px,h/2); line1 = (fin,h/2);
draw line0--line1 withcolor blue;

s0 = (fin,h/2); s1 = (fin+l_flecha,h/2);
drawarrow s0--s1 withcolor blue;

ss0 = s0; ss1 = (fin+l_flecha, h);
drawarrow ss0--ss1 withcolor blue;

sss0 = s0; sss1 = (xpart ss1, 0);
drawarrow sss0--sss1 withcolor blue;


%Out text
t = (px+0.6cm,1cm);
label("Output", t);

tt = (fin+l_flecha+0.75cm,h/2);
label("Extracts", tt);

ttt = (xpart ss1 + 1cm, ypart ss1);
label("Essential oils", ttt);

tttt = (xpart ss1+1.7cm, 0);
label("Composting material", tttt);

endfig;

%------ESQUEMA DETALLADO------
beginfig(2);
%Datos del ractángulo
hh = 3.5 cm;
anchoo = 11.3 cm;

%Input
pair lab, f[];
lab = (0, hh/2);
label("Input", lab);

init = 1.6cm;
f0 = (0.6cm, hh/2); f1 = (init, hh/2);
draw f0--f1 withcolor green;


%Rectángulo
pair lados[];
lados0 = (init, 0); lados1 = (init + anchoo, 0); 
lados2 = (init + anchoo, hh); lados3 = (init, hh);
draw
	for i=0 upto 3:
		lados[i] --
	endfor
cycle withcolor green;

%Destilación por arrastre de vapor
pair dab ,da[];
offset = 0.5 cm;
rgb = 255;
ancho_rect = 2cm;
da0 = (init+offset, offset); 
da1 = (xpart da0 + ancho_rect, ypart da0);
da2 = (xpart da1, hh-offset); da3 = (xpart da0, ypart da2);
draw
	for i=0 upto 3:
		da[i] --
	endfor
cycle dashed evenly withcolor (246,175,43)/rgb;

f2 = (init, hh/2); f3 = (init+offset, hh/2);
drawarrow f2--f3 dashed evenly withcolor green;

da4 = (xpart da0 + 1cm, ypart da3 - 1cm);
label("Steam", da4) withcolor (246,175,43)/rgb;

da5 = (xpart da4, ypart da4 - 0.5cm);
label("destillation", da5) withcolor (246,175,43)/rgb;

pair res[];
xx = xpart da0 + (xpart da1 - xpart da0)/2;
res0 = (xx, ypart da0); res1 = (xpart res0, 0);
res2 = (xpart res1, ypart res1 - 0.8cm);
res3 = (xpart res2 + 1cm, ypart res2);
draw res0--res1 dashed evenly withcolor blue;

draw res1--res2--res3 withcolor blue;

res4 = (xpart res3 + 1.25cm, ypart res3);
label("Essential oils", res4);

finn = init + anchoo + 1cm;
res5 = (xpart res4 + 1.25cm, ypart res4);
res6 = (finn-0.25cm, ypart res5);
res7 = (xpart res6, hh/2);
drawarrow res5--res6--res7 withcolor blue;

%Dry Proccess
pair dadry[] ,dry[];
dry0 = (xpart da1 + l_flecha, ypart da1); 
dry1 = (xpart dry0 + ancho_rect, ypart dry0);
dry2 = (xpart dry1, ypart da2);
dry3 = (xpart dry0, ypart dry2);
draw
	for i=0 upto 3:
		dry[i] --
	endfor
cycle dashed evenly withcolor (223, 67, 221)/rgb;

dadry0 = (xpart da1, ypart da1 + (ypart da2-ypart da1)/2);
dadry1 = (xpart dry0, ypart dadry0);
drawarrow dadry0--dadry1 dashed evenly withcolor (246,175,43)/rgb;

dry4 = (xpart dry0 + 1cm, ypart dry2 - 1cm);
label("Drying", dry4) withcolor (223, 67, 221)/rgb;
dry5 = (xpart dry4, ypart dry4 - 0.5cm);
label("process", dry5) withcolor (223, 67, 221)/rgb;

%MSPD Extraction
pair mspd[], dpm[];
dpm0 = (xpart dry2, ypart dry1 + (ypart dry2 - ypart dry1)/2);
dpm1 = (xpart dpm0 + l_flecha, ypart dpm0);
drawarrow dpm0--dpm1 dashed evenly withcolor (223, 67, 221)/rgb;

mspd0 = (xpart dpm1, ypart dry0);
mspd1 = (xpart mspd0 + ancho_rect, ypart mspd0);
mspd2 = (xpart mspd1, ypart dry2);
mspd3 = (xpart mspd0, ypart mspd2);
draw
	for i=0 upto 3:
		mspd[i] --
	endfor
cycle dashed evenly withcolor (158, 177, 199)/rgb;

mspd4 = (xpart mspd0 + 1cm, ypart mspd2 - 1cm);
label("MSPD", mspd4) withcolor (158, 177, 199)/rgb;
mspd5 = (xpart mspd4, ypart mspd4 - 0.5cm);
label("extraction", mspd5) withcolor (158, 177, 199)/rgb;

mspd6 = (xpart mspd0 + (xpart mspd1 - xpart mspd0)/2, ypart mspd2);
mspd7 = (xpart mspd6, ypart mspd6 + offset);
draw mspd6--mspd7 dashed evenly withcolor blue;

mspd8 = (xpart mspd7, ypart mspd7 + 0.5cm);
draw mspd7--mspd8 withcolor blue;

mspd9 = (xpart mspd8 + 1cm, ypart mspd8);
draw mspd8--mspd9 withcolor blue;

mspd10 = (xpart mspd9 + 0.6cm, ypart mspd9);
label("Extract", mspd10);

mspd11 = (xpart mspd10 + 0.7cm, ypart mspd10);
mspd12 = (finn-l_flecha/2, ypart mspd10);
mspd13 = (xpart mspd12, hh/2);
drawarrow mspd11--mspd12--mspd13 withcolor blue;
	
%End
pair mcp[];
mcp0 = (xpart mspd1, ypart mspd1 + (ypart mspd2 - ypart mspd1)/1.125);
mcp1 = (xpart mcp0 + (finn - l_flecha - xpart mcp0)/2, ypart mcp0);
mcp2 = (xpart mcp1, ypart mcp1 - 0.5cm);
draw mcp0--mcp1--mcp2 dashed evenly withcolor (158, 177, 199)/rgb;

mcp3 = (xpart mcp2, ypart mcp2 - 0.2cm);
label("Composting", mcp3);
mcp4 = (xpart mcp3, ypart mcp3 - 0.3cm);
label("material", mcp4);

mcp5 = (xpart mcp4, ypart mcp4 - 0.25cm);
mcp6 = (xpart mcp5, ypart mcp5 - 1cm);
draw mcp5--mcp6 dashed evenly withcolor (246,175,43)/rgb;

pair outp[];
outp0 = (xpart mcp6, ypart mcp6 + (ypart mcp5 - ypart mcp6)/2);
outp1 = (finn - l_flecha, ypart outp0);
draw outp0--outp1 dashed evenly withcolor blue;

outp2 = (xpart outp1 + 0.3cm, ypart outp1);
outp3 = (xpart outp2, hh/2);
drawarrow outp1--outp2--outp3 withcolor blue;

mcp7 = (xpart mcp6, ypart mcp6 - 0.2cm);
label("Biofuel", mcp7) withcolor (246,175,43)/rgb;

mcp8 = (xpart mcp7 - 0.55cm, ypart mcp7 - 0.05cm);
mcp9 = (xpart da1 - (xpart da1 - xpart da0)/3, ypart mcp8);
mcp10 = (xpart mcp9, ypart da0);
drawarrow mcp8--mcp9--mcp10 dashed evenly withcolor (246,175,43)/rgb;

%Output
pair labb, ff[];
ff0 = (finn-l_flecha, hh/2); ff1 = (finn, hh/2);
drawarrow ff0--ff1 withcolor blue;

labb = (finn+0.6cm, hh/2);
label("Output", labb);


endfig;
end;
