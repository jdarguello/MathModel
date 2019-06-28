beginfig(22)
z1 = (5mm,5mm);
drawarrow origin--z1;
label("Hello World!", z1) withcolor blue;
label.urt("Hello World!", z1) withcolor red;
draw thelabel.rt("Hello" & " " & "San Diego!", origin)
xscaled 0.7
rotated 60 shifted 2z1 withcolor green;
endfig;

end;