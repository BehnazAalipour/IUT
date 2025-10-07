function [Result] =MY_PSNR(Originanl_Image,Reconstructed_Image)
Result = 10*log10((1^2)/MY_MSE(Originanl_Image,Reconstructed_Image));
end