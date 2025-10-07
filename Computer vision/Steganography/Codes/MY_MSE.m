function [Result] = MY_MSE(Original_Image,Reconstructed_Image)
Error=(Original_Image(:)-Reconstructed_Image(:)).^2;
Result = sum(Error)/numel(Error);
end