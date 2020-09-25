filename = '../data/工.txt';


[movl,B,C,D,E,F,G,H,I,J] = textread(filename,'%s %d %f %f %f %f %f %f %f %s');
% C = X / D = Y / E = Z / F = roll / G = pitch / H = yaw / J = stroke

cmd_new = [C,D,E,F,G,H];      % A是Cmd
x = cmd_new(:,1) ;
y = cmd_new(:,2) ;
z = cmd_new(:,3) ;
roll = cmd_new(:,4) ;
pitch = cmd_new(:,5) ;
yaw = cmd_new(:,6) ;

[m,n] = size(cmd_new);

R06 =[];
for i = 1:m
    R06(:,:,i) = Rot('Z',cmd_new(i,6),'d')*Rot('Y',cmd_new(i,5),'d')*Rot('X',cmd_new(i,4),'d');        
end

T06 = R06;
T06(4,4,:) = 1;

for i =1:m    
    T67(:,:,i) = eye(4);
    T67(3,4,:)=185;
    for j = 1:3
       T06(j,4,i) = cmd_new(i,j); 
    end 
end

for i = 1:size(T06,3) 
    T07(:,:,i) = T06(:,:,i)*T67(:,:,i);
end

x0 = T07(1,4,:);
y0 = T07(2,4,:);
z0 = T07(3,4,:);
X = reshape(x0,[],1);              
Y = reshape(y0,[],1);
Z = reshape(z0,[],1);


figure(1);
plot(X(Z<10),Y(Z<10),'ro');
title('紅色為實際毛筆會到達的點','fontsize',12);

figure(2);
plot(X(Z<10),Y(Z<10),'b-');
title('藍色為機械手臂書寫的模擬(筆劃與筆劃間的連線可忽略)','fontsize',12);

% figure(1);
% plot(X,Y,'ro');
% title('紅色為實際毛筆會到達的點','fontsize',12);