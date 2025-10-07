clc;clear;close all;
stego_image=imread('stego_image.png');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
stego_image_1=(bitget(stego_image,1));
stego_image_2=(bitget(stego_image,2));
stego_image_3=(bitget(stego_image,3));
stego_image_4=(bitget(stego_image,4));
stego_image_5=(bitget(stego_image,5));
stego_image_6=(bitget(stego_image,6));
stego_image_7=(bitget(stego_image,7));
stego_image_8=(bitget(stego_image,8));

subplot(2,4,1)
imshow(stego_image_1,[]);
title('plan 1')
subplot(2,4,2)
imshow(stego_image_2,[]);
title('plan 2')
subplot(2,4,3)
imshow(stego_image_3,[]);
title('plan 3')
subplot(2,4,4)
imshow(stego_image_4,[]);
title('plan 4')
subplot(2,4,5)
imshow(stego_image_5,[]);
title('plan 5')
subplot(2,4,6)
imshow(stego_image_6,[]);
title('plan 6')
subplot(2,4,7)
imshow(stego_image_7,[]);
title('plan 7')
subplot(2,4,8)
imshow(stego_image_8,[]);
title('plan 8')