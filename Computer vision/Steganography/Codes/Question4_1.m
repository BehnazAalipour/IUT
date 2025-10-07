clc;clear;close all;
Key=rng;
iut=imread('IUT.jpg');
cover_image=imread('Cover_Image.png');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
imwrite(iut,'iut.png');
iut_image=imread('iut.png');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
R=iut_image(:,:,1);
G=iut_image(:,:,2);
B=iut_image(:,:,3);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


R_1=(bitget(R,1));
R_2=(bitget(R,2));
R_3=(bitget(R,3));
R_4=(bitget(R,4));
R_5=(bitget(R,5));
R_6=(bitget(R,6));
R_7=(bitget(R,7));
R_8=(bitget(R,8));
R_matrix=[R_1 R_2 R_3 R_4 ;R_5 R_6 R_7 R_8];


G_1=(bitget(G,1));
G_2=(bitget(G,2));
G_3=(bitget(G,3));
G_4=(bitget(G,4));
G_5=(bitget(G,5));
G_6=(bitget(G,6));
G_7=(bitget(G,7));
G_8=(bitget(G,8));
G_matrix=[G_1 G_2 G_3 G_4 ;G_5 G_6 G_7 G_8];

merg_R_G=[R_matrix;G_matrix];


sm_1=size(merg_R_G);
plan_one=zeros(1080,1920);
plan_one(1:sm_1(1),1:sm_1(2))=merg_R_G;


B_1=(bitget(B,1));
B_2=(bitget(B,2));
B_3=(bitget(B,3));
B_4=(bitget(B,4));
B_5=(bitget(B,5));
B_6=(bitget(B,6));
B_7=(bitget(B,7));
B_8=(bitget(B,8));
B_matrix=[B_1 B_2 B_3 B_4 ;B_5 B_6 B_7 B_8];


sm_2=size(B_matrix);
plan_two=zeros(1080,1920);
plan_two(1:sm_2(1),1:sm_2(2))=B_matrix;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Key=rng;
Randome_Pattern=(round(rand(size(cover_image)))==1);
Randomize_plan_one=xor(plan_one,Randome_Pattern);
stego_Image=bitset(cover_image,1,Randomize_plan_one);
Randomize_plan_two=xor(plan_two,Randome_Pattern);
stego_Image=bitset(stego_Image,2,Randomize_plan_two);
imwrite(stego_Image,'stego_Image.png');
save('Key');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MY_PSNR(im2double(cover_image),im2double(stego_Image));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subplot(3,3,1)
imshow(Randome_Pattern,[]);
title('Randome Pattern')
subplot(3,3,2)
imshow(Randomize_plan_one,[]);
title('Randomize plan one')
subplot(3,3,3)
imshow(Randomize_plan_two,[]);
title('Randomize plan two')
subplot(3,3,4)
imshow(cover_image,[]);
title('cover image')
subplot(3,3,5)
imshow(iut_image,[]);
title('iut image')
subplot(3,3,6)
imshow(stego_Image,[]);
title('stego Image')

