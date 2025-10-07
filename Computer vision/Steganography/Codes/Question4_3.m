clc;clear;close all;
iut_image=im2double(imread('IUT.jpg'));
extracted_image=im2double(imread('extracted_imag.png'));

MY_PSNR(iut_image,extracted_image);