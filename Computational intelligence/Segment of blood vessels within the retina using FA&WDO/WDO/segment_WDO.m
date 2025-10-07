clc;
close all;
clear all;
warning('off', 'all')
format long g;
f1=1; %Zoom level
%%%%%%%%%%%%%%%%%%%%%%%%%
I=imread('21_training.png');
img=I;
mask=imread('21_training_mask.gif');
I=uint8(I);
I=I(:,:,2);

 orig=I;
 dis=I;
 I=imsharpen(I,'Radius',5,'Amount',10);
 %I=adapthisteq(I);
 %I=imsharpen(Gmag,'Radius',5,'Amount',10);
[his, bin]=imhist(I);

% User defined WDO parameters:
npop = 15;              % population size.
nVar =3 ;               % Dimension of the problem.
maxit = 100;            % Maximum number of iterations.
param.RT = 3;			% RT coefficient.
param.g = 0.2;			% gravitational constant.
param.alp = 0.4;		% constants in the update eq.
param.c = 0.4;			% coriolis effect.
maxV = 70;              % maximum allowed speed.
varMin =  1;			% Lower dimension boundary.
varMax= numel(his);		% Upper dimension boundary.
%---------------------------------------------------------------
tic
% Initialize WDO population, position and velocity:
p=randi([varMin,varMax],[1 nVar npop]);

for i=1:npop
    pos(i,:) = p(:,:,i); % Randomize velocity:
end

vel=zeros(npop, nVar);

% Evaluate initial population:
for K=1:npop,
   	pres(K,:) = otsu(his, pos(K,:));
end
%----------------------------------------------------------------

% Finding best air parcel in the initial population :
[globalpres,indx] = max(pres);
globalpos = pos(indx,:);
maxpres(1) = max(pres);			% maximum pressure


% Rank the air parcels:
[sorted_pres, rank_ind] = sort(pres, 'descend');
% Sort the air parcels:
pos = pos(rank_ind,:);
keepglob(1) = globalpres;



iter = 1;   % iteration counter
for ij = 2:maxit,
    	% Update the velocity:
    	for i=1:npop
		% choose random dimensions:
		a = randperm(nVar);        			
		% choose velocity based on random dimension:
    		velot(i,:) = vel(i,a);				
        	vel(i,:) = (1-param.alp)*vel(i,:)-(param.g*pos(i,:))+ ...
				    abs(1-1/i)*((globalpos-pos(i,:)).*param.RT)+ ...
				    (param.c*velot(i,:)/i);
    	end
    
        	% Check velocity:
        	vel = min(vel, maxV);
        	vel = max(vel, -maxV);
		% Update air parcel positions:
    		pos = pos + vel;
        	pos = round(min(pos, varMax));
        	pos = max(pos, varMin); 
		% Evaluate population: (Pressure)
		for K=1:npop,
				pres(K,:) = otsu(his, pos(K,:));
		end

    	%----------------------------------------------------
    	% Finding best particle in population
    	[maxpres,indx] = max(pres);
    	maxpos = pos(indx,:);           	% min location for this iteration
    	%----------------------------------------------------
    	% Rank the air parcels:
    	[sorted_pres, rank_ind] = sort(pres);
    	% Sort the air parcels position, velocity and pressure:
    	pos = pos(rank_ind,:);
    	vel = vel(rank_ind,:);
    	pres = sorted_pres;  
    
    	% Updating the global best:
    	better = maxpres > globalpres;
    	if better
        		globalpres = maxpres;             % initialize global minimum
        		globalpos = maxpos;
   	end
	% Keep a record of the progress:
    	keepglob(ij) = globalpres;    	
end
elapsedTime = toc;
fprintf('Elapsed time: %.4f seconds\n', elapsedTime);

pressure = transpose(keepglob);
a=sort(globalpos);
levels=a-[ones(1,nVar)];
imq=imquantize(I,levels);
imq=imq-1;
imf=uint8(imq*(255/nVar));
imf=imf.*mask;

figure;
plot(keepglob,'--k','linewidth',1);
title('WDO Train');
xlabel('WDO Iteration Number');
ylabel('WDO Best Cost Value');
figure;
%subplot(1,2,1);
%imshow(img);title('Original');
%subplot(1,2,2);
imshow(imf,[]);title('Segmented Image WDO');
