clc
clear
close all
% filename = '../data/char00644_stroke.txt';
% 當前目錄下的檔案
in_dir = '../data'
out_dir = '../output'
files = dir(in_dir);
% 檔案數量
len = length(files);
name = {};
index = 1;
for ii = 1 : len
    % 跳過.以及..資料夾
    if (strcmp(files(ii).name, '.') == 1) ...
            || (strcmp(files(ii).name, '..') == 1)
        continue;
    end
    % 讀取指定型別的檔案(可根據自己需要修改)
    if ~isempty(strfind(files(ii).name, '.txt'))
        name{index} = fullfile(in_dir, '\', files(ii).name);
        save_name = fullfile(out_dir, '\', files(ii).name);
        fid=fopen(save_name,'w');
        
        [movl,B,C,D,E,F,G,H,I,J] = textread(name{index},'%s %d %f %f %f %f %f %f %f %s');
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
            R06(:,:,i) = Rot('Z',cmd_new(i,6),'d')*Rot('Y',cmd_new(i,5),'d')*Rot('X',cmd_new(i,4),'d')      
        end

        T06 = R06;
        T06(4,4,:) = 1;
        T67 = [];
        for i =1:m    
            T67(:,:,i) = eye(4);
            T67(3,4,:)=185;
            for j = 1:3
               T06(j,4,i) = cmd_new(i,j); 
            end 
        end
        T07 = [];
        for i = 1:size(T06,3) 
            T07(:,:,i) = T06(:,:,i)*T67(:,:,i);
        end

        x0 = T07(1,4,:);
        y0 = T07(2,4,:);
        z0 = T07(3,4,:);
        X = reshape(x0,[],1);              
        Y = reshape(y0,[],1);
        Z = reshape(z0,[],1);

        % Write data to text file
        dlmwrite(save_name, [X Y], 'delimiter',' ')
        % dlmwrite(save_name, [X Y Z], 'delimiter',' ')
        
        index = index + 1;
    end
end