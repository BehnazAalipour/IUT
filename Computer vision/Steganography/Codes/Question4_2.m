clc;clear;
load 'key'
stego_Image=imread('stego_Image.png');
rng(Key);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Randome_Patt =round(rand(size(stego_Image)));
LSB_1=(bitget(stego_Image,1)==1);
LSB_2=(bitget(stego_Image,2)==1);
extracted_plan_1=uint8(xor(LSB_1,Randome_Patt));
extracted_plan_2=uint8(xor(LSB_2,Randome_Patt));

R=uint8(zeros(267,400));
G=uint8(zeros(267,400));
B=uint8(zeros(267,400));

A=uint8(zeros(267,400));

start_rows=1;
end_rows=267;

start_cols=1;
end_cols=400;

i=1;
while end_rows <= 534
      while end_cols <= 1600
           A=extracted_plan_1(start_rows:end_rows,start_cols:end_cols);
           R=bitset(R,i,A);
           start_cols = start_cols+400;
           end_cols = end_cols+400;
           i =i+1;
       end
       start_rows =start_rows+267;
       end_rows = end_rows +267;
       start_cols=1;
       end_cols=400;
end

start_rows=535;
end_rows=801;

start_cols=1;
end_cols=400;

i=1;
while end_rows <= 1068
     while end_cols <= 1600
            A=extracted_plan_1(start_rows:end_rows,start_cols:end_cols);
            G=bitset(G,i,A);
            start_cols = start_cols + 400;
            end_cols = end_cols + 400;
            i=i+1;
      end
       start_rows =start_rows+267;
       end_rows = end_rows +267;
       start_cols=1;
       end_cols=400;
end

start_rows=1;
end_rows=267;

start_cols=1;
end_cols=400;
i=1;
   while end_rows <= 534
       while end_cols <= 1600
            A=extracted_plan_2(start_rows:end_rows,start_cols:end_cols);
            B=bitset(B,i,A);
            start_cols = start_cols+400;
            end_cols = end_cols+400;
            i=i+1;
       end
       start_rows =start_rows+267;
       end_rows = end_rows +267;
       start_cols=1;
       end_cols=400;
   end

extracted_image=cat(3,R,G,B);
imshow(extracted_image);

imwrite(extracted_image,'extracted_imag.png');
