
t=6/10;ia=2.7/10;ib=5.4/10;ts=0.6/10;br=7.5/10;

a=12.394588/10;
b=40.74236667298/10;
D=33.323602552132/10;


def buildcavity(f1):
    """
    Generates a Superfish input file for a cavity with specified parameters.
    
    Parameters:
    f1 (str): The name of the output file to write the Superfish input.
    """
    # Open the file for writing
    with open(f1, 'w') as fid:
        fid.write('Resonant frequency search for 2Pi/3 mode at 2998.8 MHz\n')
        fid.write('\n')
        fid.write('&reg kprob=1,     ; Superfish problem\n')
        fid.write('freq=2998.8,      ; Frequency in MHz\n')
        fid.write('nbsup=1,          ; Upper boundary\n')
        fid.write('nbslo=0,          ; Lower boundary\n')
        fid.write('nbsrt=1,          ; Right boundary\n')
        fid.write('nbslf=1,          ; Left boundary\n')
        fid.write('dx=0.01,          ; Mesh spacing\n')
        fid.write('dy=0.01,          ; Mesh spacing\n')
        fid.write('xdri=3.332360,    ; Drive point X coordinate \n')
        fid.write('ydri=3.9,         ; Drive point Y coordinate \n')
        fid.write('kmethod=1,        ; Use beta to compute wave number \n')
        fid.write('dslope=-1,        ; Allows FISH to converge in 1 iteration \n')
        fid.write(f'zctr={D*1.5/2},    ; Reference Z in transit-time integrals \n')
        fid.write('beta=1.00&        ; Particle velocity for transit-time integrals \n\n\n\n')

        fid.write(';Number of cavities is 1.5\n\n')
        
        # Define the points for the cavity
        fid.write('&po x=0, y=0 &;\n')
        fid.write(f'&po x=0, y={b} &;\n')
        fid.write(f'&po x={(D-t)/2-br}, y={b} &;\n')
        fid.write(f'&po nt=2, x0={(D-t)/2-br}, y0={b-br}, x={br}, y=0 &;\n')
        fid.write(f'&po x={(D-t)/2}, y={a+ib} &;\n')
        fid.write(f'&po nt=2, x0={(D-t)/2+ia}, y0={a+ib}, a={ia}, aovrb={ia/ib}, x=0, y={-ib} &;\n')
        fid.write(f'&po x={(D-t)/2+ia+ts}, y={a} &;\n')
        fid.write(f'&po nt=2, x0={(D-t)/2+ia+ts}, y0={a+ib}, a={ia}, aovrb={ia/ib}, x={ia}, y=0 &;\n')
        fid.write(f'&po x={D/2+t/2}, y={b-br} &;\n')
        fid.write(f'&po nt=2, x0={D/2+t/2+br}, y0={b-br}, x=0, y={br} &;\n')
        fid.write(f'&po x={1.5*D-t/2-br}, y={b} &;\n')
        fid.write(f'&po nt=2, x0={1.5*D-t/2-br}, y0={b-br}, x={br}, y=0 &;\n')
        fid.write(f'&po x={1.5*D-t/2}, y={a+ib} &;\n')
        fid.write(f'&po nt=2, x0={1.5*D-t/2+ia}, y0={a+ib}, a={ia}, aovrb={ia/ib}, x=0, y={-ib} &;\n')
        fid.write(f'&po x={1.5*D}, y={a} &;\n')
        fid.write(f'&po x={1.5*D}, y=0 &;\n')
        fid.write('&po x=0, y=0 &;\n')
        fid.write('\n')
    print(f"Superfish input file '{f1}' created successfully.")
if __name__ == "__main__":
    buildcavity('cavity_input.af')
# fid=fopen(f1,'w');
# fprintf(fid,'Resonant frequency search for 2Pi/3 mode at 2998.8 MHz\n');
# fprintf(fid,'\n');
# fprintf(fid,'&reg kprob=1,     ; Superfish problem\n');
# fprintf(fid,'freq=2998.8,      ; Frequency in MHz\n');
# fprintf(fid,'nbsup=1,          ; Upper boundary\n');
# fprintf(fid,'nbslo=0,          ; Lower boundary\n');
# fprintf(fid,'nbsrt=1,          ; Right boundary\n');
# fprintf(fid,'nbslf=1,          ; Left boundary\n');
# fprintf(fid,'dx=0.01,          ; Mesh spacing\n');
# fprintf(fid,'dy=0.01,          ; Mesh spacing\n');
# fprintf(fid,'xdri=3.332360,    ; Drive point X coordinate \n');
# fprintf(fid,'ydri=3.9,         ; Drive point Y coordinate \n');
# fprintf(fid,'kmethod=1,        ; Use beta to compute wave number \n');
# fprintf(fid,'dslope=-1,        ; Allows FISH to converge in 1 iteration \n');
# fprintf(fid,'zctr=%f,    ; Reference Z in transit-time integrals \n', D*1.5/2);
# fprintf(fid,'beta=1.00&        ; Particle velocity for transit-time integrals \n\n\n\n');

# fprintf(fid,';Number of cavities is 1.5\n\n');
# fprintf(fid,'&po x=0, y=0 &;\n');
# fprintf(fid,'&po x=0, y=%f &;\n',b);

# fprintf(fid,'&po x=%f, y=%f &;\n',(D-t)/2-br,b);
# fprintf(fid,'&po nt=2, x0=%f, y0=%f, x=%f, y=%f &;\n',(D-t)/2-br,b-br,br,0);
# fprintf(fid,'&po x=%f, y=%f &;\n',(D-t)/2,a+ib);
# fprintf(fid,'&po nt=2, x0=%f, y0=%f, a=%f, aovrb=%f, x=%f, y=%f &;\n',(D-t)/2+ia,a+ib,ia,ia/ib,0,-ib);
# fprintf(fid,'&po x=%f, y=%f &;\n',(D-t)/2+ia+ts,a);
# fprintf(fid,'&po nt=2, x0=%f, y0=%f, a=%f, aovrb=%f, x=%f, y=%f &;\n',(D-t)/2+ia+ts,a+ib,ia,ia/ib,ia,0);
# fprintf(fid,'&po x=%f, y=%f &;\n',D/2+t/2,b-br);
# fprintf(fid,'&po nt=2, x0=%f, y0=%f, x=%f, y=%f &;\n',D/2+t/2+br,b-br,0,br);
# fprintf(fid,'&po x=%f, y=%f &;\n',1.5*D-t/2-br,b);
# fprintf(fid,'&po nt=2, x0=%f, y0=%f, x=%f, y=%f &;\n',1.5*D-t/2-br,b-br,br,0);
# fprintf(fid,'&po x=%f, y=%f &;\n',1.5*D-t/2,a+ib);
# fprintf(fid,'&po nt=2, x0=%f, y0=%f, a=%f, aovrb=%f, x=%f, y=%f &;\n',1.5*D-t/2+ia,a+ib,ia,ia/ib,0,-ib);
# fprintf(fid,'&po x=%f, y=%f &;\n',1.5*D,a);

# fprintf(fid,'&po x=%f, y=%f &;\n',1.5*D,0);
# fprintf(fid,'&po x=%f, y=%f &;\n',0,0);
