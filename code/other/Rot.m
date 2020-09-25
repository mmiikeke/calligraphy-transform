function R=Rot(axis,degree,type)
% Rot('Z',90,'d')
if nargin==2
    type='d';
end

if strcmpi(type,'d')    %degree
    d=degree*pi/180;
elseif strcmpi(type,'r')    %rad
    d=degree;
else 
    error('error type string')
end
c=@cos;
s=@sin;

if strcmpi(axis,'X') || strcmpi(axis,'x')
    R=[1        0        0;
       0        c(d)    -s(d);
       0        s(d)     c(d)];
   cad = c(d);
   sad = s(d);
   
elseif strcmpi(axis,'Y') || strcmpi(axis,'y')
    R=[c(d)     0       s(d);
        0       1        0;
       -s(d)	0       c(d)];
   cbd = c(d);
   sbd = s(d);
elseif strcmpi(axis,'Z') || strcmpi(axis,'z')
    R=[c(d)     -s(d)       0;
       s(d)     c(d)        0;
       0        0           1];
   ccd = c(d);
   scd = s(d);
else 
    error('error axis string')
  
end